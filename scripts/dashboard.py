"""Runtime dashboard: đọc data/logs.jsonl, tính 6 panel theo config/dashboard.yaml, xuất HTML tĩnh.

    python scripts/dashboard.py                 # tạo data/dashboard.html một lần
    python scripts/dashboard.py --watch         # tạo lại mỗi refresh_seconds (trang tự reload)
    python scripts/dashboard.py --end latest    # cửa sổ 60 phút kết thúc ở log mới nhất
"""
from __future__ import annotations

import argparse
import html
import json
import math
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import mean
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.cli import configure_utf8_stdio
from app.metrics import percentile

Series = list[float | None]


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

def load_records(path: Path) -> list[dict[str, Any]]:
    """Đọc JSONL, bỏ dòng hỏng, gắn `_ts` (datetime UTC) cho mỗi record."""
    records = []
    if not path.exists():
        return records
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            record = json.loads(line)
            record["_ts"] = datetime.fromisoformat(record["ts"]).astimezone(timezone.utc)
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            continue
        records.append(record)
    return records


def _pct(part: int, total: int) -> float | None:
    return round(part / total * 100, 2) if total else None


def _cumulative(values: list[float]) -> list[float]:
    out, running = [], 0.0
    for value in values:
        running += value
        out.append(round(running, 6))
    return out


def compute_panels(records: list[dict[str, Any]], start: datetime, minutes: int) -> dict[str, dict[str, Any]]:
    """Tính summary + chuỗi theo phút cho 6 panel trong cửa sổ [start, start + minutes)."""
    end = start + timedelta(minutes=minutes)
    buckets: list[list[dict[str, Any]]] = [[] for _ in range(minutes)]
    for record in records:
        if start <= record["_ts"] < end:
            buckets[int((record["_ts"] - start).total_seconds() // 60)].append(record)
    window = [record for bucket in buckets for record in bucket]

    def events(rows: list[dict[str, Any]], name: str) -> list[dict[str, Any]]:
        return [row for row in rows if row.get("event") == name]

    def values(rows: list[dict[str, Any]], field: str) -> list[Any]:
        return [row[field] for row in rows if row.get(field) is not None]

    def per_minute(fn) -> Series:
        return [fn(bucket) for bucket in buckets]

    sent = events(window, "response_sent")
    received = events(window, "request_received")
    failed = events(window, "request_failed")
    tool_results = values(window, "tool_success")

    def pctl(field: str, p: int):
        return lambda rows: percentile(values(events(rows, "response_sent"), field), p) if events(rows, "response_sent") else None

    def error_rate(rows):
        return _pct(len(events(rows, "request_failed")), len(events(rows, "request_received")))

    def tool_rate(rows):
        results = values(rows, "tool_success")
        return _pct(sum(1 for ok in results if ok), len(results))

    def field_sum(field: str):
        return lambda rows: float(sum(values(events(rows, "response_sent"), field)))

    def quality(rows):
        scores = values(events(rows, "response_sent"), "quality_score")
        return round(mean(scores), 4) if scores else None

    tokens_in = sum(values(sent, "tokens_in"))
    tokens_out = sum(values(sent, "tokens_out"))
    error_breakdown: dict[str, int] = {}
    for row in failed:
        error_breakdown[row.get("error_type") or "unknown"] = error_breakdown.get(row.get("error_type") or "unknown", 0) + 1
    quality_scores = values(sent, "quality_score")

    return {
        "latency": {
            "summary": {
                "p50": percentile(values(sent, "latency_ms"), 50),
                "p95": percentile(values(sent, "latency_ms"), 95),
                "p99": percentile(values(sent, "latency_ms"), 99),
                "ttft_p95": percentile(values(sent, "ttft_ms"), 95),
            },
            "series": {
                "p50": per_minute(pctl("latency_ms", 50)),
                "p95": per_minute(pctl("latency_ms", 95)),
                "p99": per_minute(pctl("latency_ms", 99)),
                "ttft_p95": per_minute(pctl("ttft_ms", 95)),
            },
        },
        "traffic": {
            "summary": {"count": len(received), "rate_per_minute": round(len(received) / minutes, 2)},
            "series": {"requests": per_minute(lambda rows: float(len(events(rows, "request_received"))))},
        },
        "errors": {
            "summary": {
                "error_rate_pct": _pct(len(failed), len(received)),
                "count_by_value": error_breakdown,
                "tool_success_rate_pct": _pct(sum(1 for ok in tool_results if ok), len(tool_results)),
            },
            "series": {
                "error_rate_pct": per_minute(error_rate),
                "tool_success_rate_pct": per_minute(tool_rate),
            },
        },
        "cost": {
            "summary": {"total": round(sum(values(sent, "cost_usd")), 6)},
            "series": {"cumulative": _cumulative(per_minute(field_sum("cost_usd")))},
            "table": {"sum_by_minute": per_minute(field_sum("cost_usd"))},
        },
        "tokens": {
            "summary": {"tokens_in": tokens_in, "tokens_out": tokens_out, "sum_by_field": max(tokens_in, tokens_out)},
            "series": {
                "tokens_in": _cumulative(per_minute(field_sum("tokens_in"))),
                "tokens_out": _cumulative(per_minute(field_sum("tokens_out"))),
            },
        },
        "quality": {
            "summary": {"mean": round(mean(quality_scores), 4) if quality_scores else None},
            "series": {"mean": per_minute(quality)},
        },
    }


def check_threshold(panel: dict[str, Any], threshold: dict[str, Any]) -> tuple[float | None, bool | None]:
    """Trả về (giá trị quan sát, đạt ngưỡng?) cho aggregation mà contract chỉ định."""
    observed = panel["summary"].get(threshold["aggregation"])
    if observed is None:
        return None, None
    ok = observed <= threshold["value"] if threshold["operator"] == "lte" else observed >= threshold["value"]
    return observed, ok


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

SERIES_LABELS = {
    "p50": "Latency P50", "p95": "Latency P95", "p99": "Latency P99", "ttft_p95": "TTFT P95",
    "requests": "Requests", "error_rate_pct": "Error rate", "tool_success_rate_pct": "Retrieval success",
    "cumulative": "Cumulative cost", "tokens_in": "Tokens in", "tokens_out": "Tokens out",
    "mean": "Mean quality",
}
SUMMARY_LABELS = {
    "p50": "P50", "p95": "P95", "p99": "P99", "ttft_p95": "TTFT P95", "count": "Requests",
    "rate_per_minute": "Avg rate", "error_rate_pct": "Error rate",
    "tool_success_rate_pct": "Retrieval success", "total": "Total cost", "tokens_in": "Tokens in",
    "tokens_out": "Tokens out", "mean": "Mean quality",
}
UNIT_SUFFIX = {"ms": " ms", "percent": "%", "requests_per_minute": "/min", "usd": "", "tokens": "", "score_0_to_1": ""}
OPERATOR_TEXT = {"lte": "≤", "gte": "≥"}


def fmt(value: float | None, unit: str) -> str:
    if value is None:
        return "–"
    if unit == "usd":
        return f"${value:,.4f}"
    if unit == "score_0_to_1":
        return f"{value:.2f}"
    if unit == "ms" or unit == "tokens":
        return f"{value:,.0f}{UNIT_SUFFIX[unit]}"
    return f"{value:,.2f}".rstrip("0").rstrip(".") + UNIT_SUFFIX.get(unit, "")


def axis_ticks(data_max: float, unit: str) -> list[float]:
    """Mốc trục y tròn (bước 1/2/5 x 10^k); trục phần trăm cố định 0–100."""
    if unit == "percent":
        return [0, 25, 50, 75, 100]
    if unit == "score_0_to_1":
        return [0, 0.25, 0.5, 0.75, 1.0]
    raw = max(data_max, 1e-9) / 4
    magnitude = 10 ** math.floor(math.log10(raw))
    step = next(m * magnitude for m in (1, 2, 5, 10) if raw <= m * magnitude)
    return [round(step * k, 10) for k in range(math.ceil(data_max / step) + 1)]


def fmt_tick(value: float, unit: str) -> str:
    text = f"{value:,g}"
    return f"${text}" if unit == "usd" else text + UNIT_SUFFIX.get(unit, "")


def svg_chart(labels: list[str], series: dict[str, Series], threshold: dict[str, Any], unit: str) -> str:
    width, height, left, right, top, bottom = 560, 220, 64, 12, 12, 26
    plot_w, plot_h = width - left - right, height - top - bottom
    points = [v for s in series.values() for v in s if v is not None]
    ticks = axis_ticks(max(points + [threshold["value"]]) * 1.05, unit)
    y_max = ticks[-1]
    n = len(labels)
    x = lambda i: left + (i + 0.5) * plot_w / n
    y = lambda v: top + plot_h - v / y_max * plot_h
    parts = [f'<svg viewBox="0 0 {width} {height}" role="img" class="chart">']

    for value in ticks:  # gridlines + y ticks
        parts.append(f'<line class="grid" x1="{left}" x2="{width - right}" y1="{y(value):.1f}" y2="{y(value):.1f}"/>')
        parts.append(f'<text class="tick" x="{left - 6}" y="{y(value) + 4:.1f}" text-anchor="end">{html.escape(fmt_tick(value, unit))}</text>')
    for i in range(0, n, 10):
        parts.append(f'<text class="tick" x="{x(i):.1f}" y="{height - 6}" text-anchor="middle">{labels[i]}</text>')

    ty = y(threshold["value"])  # threshold / SLO line
    parts.append(f'<line class="threshold" x1="{left}" x2="{width - right}" y1="{ty:.1f}" y2="{ty:.1f}"/>')
    parts.append(
        f'<text class="threshold-label" x="{width - right - 4}" y="{ty - 5:.1f}" text-anchor="end">'
        f'threshold {OPERATOR_TEXT[threshold["operator"]]} {html.escape(fmt(threshold["value"], unit))}</text>'
    )

    for slot, (name, values) in enumerate(series.items(), start=1):
        segment: list[str] = []
        segments: list[list[str]] = []
        for i, value in enumerate(values):
            if value is None:
                if segment:
                    segments.append(segment)
                segment = []
            else:
                segment.append(f"{x(i):.1f},{y(value):.1f}")
        if segment:
            segments.append(segment)
        for seg in segments:
            if len(seg) > 1:
                parts.append(f'<polyline class="line s{slot}" points="{" ".join(seg)}"/>')
        last = max((i for i, v in enumerate(values) if v is not None), default=None)
        for i, value in enumerate(values):
            if value is None:
                continue
            isolated = (i == 0 or values[i - 1] is None) and (i == n - 1 or values[i + 1] is None)
            tip = f"{labels[i]} · {SERIES_LABELS[name]}: {fmt(value, unit)}"
            if isolated or i == last:
                parts.append(f'<circle class="dot s{slot}" cx="{x(i):.1f}" cy="{y(value):.1f}" r="4"/>')
            parts.append(f'<circle class="hit" cx="{x(i):.1f}" cy="{y(value):.1f}" r="9"><title>{html.escape(tip)}</title></circle>')
    parts.append("</svg>")
    return "".join(parts)


def render_panel(spec: dict[str, Any], panel: dict[str, Any], labels: list[str]) -> str:
    unit, threshold = spec["unit"], spec["threshold"]
    observed, ok = check_threshold(panel, threshold)
    if ok is None:
        status = '<span class="status nodata">○ No data</span>'
    elif ok:
        status = '<span class="status ok"><span class="icon">✓</span> Within threshold</span>'
    else:
        status = '<span class="status breach"><span class="icon">✕</span> Threshold breached</span>'

    stats = []
    for key, value in panel["summary"].items():
        if key == "sum_by_field":
            continue
        if key == "count_by_value":
            text = ", ".join(f"{k}: {v}" for k, v in value.items()) or "none"
            stats.append(f'<div class="stat"><div class="stat-label">Errors by type</div><div class="stat-value small">{html.escape(text)}</div></div>')
            continue
        stat_unit = "percent" if key in ("error_rate_pct", "tool_success_rate_pct") else "tokens" if key == "count" else unit
        stats.append(
            f'<div class="stat"><div class="stat-label">{SUMMARY_LABELS[key]}</div>'
            f'<div class="stat-value">{html.escape(fmt(value, stat_unit))}</div></div>'
        )

    legend = ""
    if len(panel["series"]) > 1:
        legend = '<div class="legend">' + "".join(
            f'<span class="key"><span class="swatch s{i}"></span>{SERIES_LABELS[name]}</span>'
            for i, name in enumerate(panel["series"], start=1)
        ) + "</div>"

    table_series = {**panel["series"], **panel.get("table", {})}
    rows = [
        "<tr><td>" + labels[i] + "</td>" + "".join(f"<td>{html.escape(fmt(s[i], unit))}</td>" for s in table_series.values()) + "</tr>"
        for i in range(len(labels))
        if any(s[i] not in (None, 0.0) for s in panel["series"].values())
    ]
    head = "".join(f"<th>{SERIES_LABELS.get(name, name.replace('_', ' '))}</th>" for name in table_series)
    table = (
        f'<details><summary>Data table ({len(rows)} minutes with data)</summary>'
        f'<table><thead><tr><th>Minute</th>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></details>'
    )

    rule = f'{threshold["aggregation"]} {OPERATOR_TEXT[threshold["operator"]]} {fmt(threshold["value"], unit)}'
    return (
        f'<section class="panel" id="{spec["id"]}"><header><div><h2>{html.escape(spec["title"])}</h2>'
        f'<div class="meta">Unit: {unit} · Threshold: {html.escape(rule)} · observed {html.escape(fmt(observed, unit if threshold["aggregation"] != "error_rate_pct" else "percent"))}</div></div>{status}</header>'
        f'<div class="stats">{"".join(stats)}</div>{legend}'
        f'{svg_chart(labels, panel["series"], threshold, unit)}{table}</section>'
    )


CSS = """
.viz-root{color-scheme:light;--page:#f9f9f7;--surface-1:#fcfcfb;--text-primary:#0b0b0b;--text-secondary:#52514e;
--muted:#898781;--grid:#e1e0d9;--border:rgba(11,11,11,.10);--series-1:#2a78d6;--series-2:#eb6834;--series-3:#1baf7a;
--series-4:#eda100;--good:#006300;--critical:#d03b3b}
@media (prefers-color-scheme:dark){:root:where(:not([data-theme="light"])) .viz-root{color-scheme:dark;--page:#0d0d0d;
--surface-1:#1a1a19;--text-primary:#fff;--text-secondary:#c3c2b7;--grid:#2c2c2a;--border:rgba(255,255,255,.10);
--series-1:#3987e5;--series-2:#d95926;--series-3:#199e70;--series-4:#c98500;--good:#0ca30c;--critical:#e66767}}
:root[data-theme="dark"] .viz-root{color-scheme:dark;--page:#0d0d0d;--surface-1:#1a1a19;--text-primary:#fff;
--text-secondary:#c3c2b7;--grid:#2c2c2a;--border:rgba(255,255,255,.10);--series-1:#3987e5;--series-2:#d95926;
--series-3:#199e70;--series-4:#c98500;--good:#0ca30c;--critical:#e66767}
*{box-sizing:border-box}body{margin:0;background:#f9f9f7}
.viz-root{min-height:100vh;background:var(--page);color:var(--text-primary);font:14px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif;padding:20px 16px}
.top h1{font-size:20px;margin:0 0 4px}.top .meta{margin-bottom:16px}
.meta{color:var(--text-secondary);font-size:12.5px}
.grid-panels{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,520px),1fr));gap:16px}
.panel{min-width:0;background:var(--surface-1);border:1px solid var(--border);border-radius:10px;padding:14px 16px}
.panel header{display:flex;flex-wrap:wrap;justify-content:space-between;gap:4px 12px;align-items:flex-start}
.panel h2{font-size:15px;margin:0 0 2px}
.status{white-space:nowrap;font-size:12.5px;font-weight:600;color:var(--text-primary)}
.status .icon{display:inline-block;width:18px;height:18px;border-radius:50%;text-align:center;line-height:18px;color:#fff;font-size:11px}
.status.ok .icon{background:var(--good)}.status.breach .icon{background:var(--critical)}.status.nodata{color:var(--muted)}
.stats{display:flex;flex-wrap:wrap;gap:6px 22px;margin:10px 0 6px}
.stat-label{color:var(--text-secondary);font-size:12px}.stat-value{font-size:20px;font-weight:600}.stat-value.small{font-size:13px;font-weight:500;padding-top:5px}
.legend{display:flex;flex-wrap:wrap;gap:4px 16px;font-size:12.5px;color:var(--text-secondary);margin:4px 0}
.key{display:inline-flex;align-items:center;gap:6px}.swatch{width:14px;height:3px;border-radius:2px;display:inline-block}
.swatch.s1{background:var(--series-1)}.swatch.s2{background:var(--series-2)}.swatch.s3{background:var(--series-3)}.swatch.s4{background:var(--series-4)}
.chart{width:100%;height:auto;display:block;margin-top:4px}
.chart .grid{stroke:var(--grid);stroke-width:1}.chart .tick{fill:var(--muted);font-size:11px;font-variant-numeric:tabular-nums}
.chart .threshold{stroke:var(--text-secondary);stroke-width:1.5;stroke-dasharray:6 4}
.chart .threshold-label{fill:var(--text-secondary);font-size:11px;font-weight:600}
.chart .line{fill:none;stroke-width:2;stroke-linejoin:round;stroke-linecap:round}
.chart .dot{stroke:var(--surface-1);stroke-width:2}.chart .hit{fill:transparent}
.chart .line.s1{stroke:var(--series-1)}.chart .line.s2{stroke:var(--series-2)}.chart .line.s3{stroke:var(--series-3)}.chart .line.s4{stroke:var(--series-4)}
.chart .dot.s1{fill:var(--series-1)}.chart .dot.s2{fill:var(--series-2)}.chart .dot.s3{fill:var(--series-3)}.chart .dot.s4{fill:var(--series-4)}
details{margin-top:8px;font-size:12.5px;color:var(--text-secondary)}summary{cursor:pointer}
table{border-collapse:collapse;margin-top:6px;width:100%;font-variant-numeric:tabular-nums}
th,td{text-align:right;padding:3px 8px;border-bottom:1px solid var(--grid)}th:first-child,td:first-child{text-align:left}
"""


def render_html(config: dict[str, Any], panels: dict[str, dict[str, Any]], start: datetime, minutes: int,
                source: Path, record_count: int) -> str:
    dashboard = config["dashboard"]
    local = lambda dt: dt.astimezone()
    labels = [local(start + timedelta(minutes=i)).strftime("%H:%M") for i in range(minutes)]
    end = start + timedelta(minutes=minutes)
    offset = local(end).strftime("%z")
    body = "".join(render_panel(spec, panels[spec["id"]], labels) for spec in dashboard["panels"])
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="refresh" content="{dashboard['refresh_seconds']}">
<title>Day 13 Dashboard</title><style>{CSS}</style></head>
<body><div class="viz-root"><div class="top"><h1>{html.escape(dashboard['title'])}</h1>
<div class="meta">Time range: last {minutes} min · {local(start):%Y-%m-%d %H:%M} – {local(end):%H:%M} (UTC{offset[:3]}:{offset[3:]})
 · Refresh: {dashboard['refresh_seconds']}s · Source: {html.escape(source.as_posix())} ({record_count} records in window)
 · Generated {local(datetime.now(timezone.utc)):%H:%M:%S}</div></div>
<div class="grid-panels">{body}</div></div></body></html>"""


def build(args: argparse.Namespace) -> Path:
    config = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    minutes = config["dashboard"]["time_range_minutes"]
    records = load_records(args.logs)
    if args.end == "latest" and records:
        end = max(r["_ts"] for r in records) + timedelta(seconds=1)
    elif args.end in ("now", "latest"):
        end = datetime.now(timezone.utc)
    else:
        end = datetime.fromisoformat(args.end).astimezone(timezone.utc)
    end = end.replace(second=0, microsecond=0) + timedelta(minutes=1)  # cửa sổ gồm cả phút hiện tại
    start = end - timedelta(minutes=minutes)
    in_window = [r for r in records if start <= r["_ts"] < end]
    panels = compute_panels(records, start, minutes)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render_html(config, panels, start, minutes, args.logs, len(in_window)), encoding="utf-8")
    return args.out


def main() -> None:
    configure_utf8_stdio()
    parser = argparse.ArgumentParser(description="Dựng dashboard 6 panel từ data/logs.jsonl")
    parser.add_argument("--logs", type=Path, default=Path("data/logs.jsonl"))
    parser.add_argument("--config", type=Path, default=REPO_ROOT / "config" / "dashboard.yaml")
    parser.add_argument("--out", type=Path, default=Path("data/dashboard.html"))
    parser.add_argument("--end", default="now", help="now (mặc định), latest, hoặc ISO timestamp")
    parser.add_argument("--watch", action="store_true", help="Tạo lại dashboard mỗi refresh_seconds")
    args = parser.parse_args()

    out = build(args)
    print(f"Dashboard: {out.resolve().as_uri()}")
    if args.watch:
        refresh = yaml.safe_load(args.config.read_text(encoding="utf-8"))["dashboard"]["refresh_seconds"]
        print(f"Đang theo dõi {args.logs}, cập nhật mỗi {refresh}s (Ctrl+C để dừng)")
        while True:
            time.sleep(refresh)
            build(args)


if __name__ == "__main__":
    main()
