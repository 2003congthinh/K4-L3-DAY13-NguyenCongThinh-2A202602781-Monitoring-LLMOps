from __future__ import annotations

from datetime import datetime, timedelta, timezone

from scripts.dashboard import check_threshold, compute_panels

START = datetime(2026, 9, 30, 4, 0, tzinfo=timezone.utc)


def record(minute: int, event: str, **fields) -> dict:
    return {"_ts": START + timedelta(minutes=minute, seconds=10), "event": event, **fields}


def sample_records() -> list[dict]:
    ok = dict(tool_name="retrieval", tool_success=True, ttft_ms=50, tokens_in=30, tokens_out=100, cost_usd=0.002)
    return [
        record(0, "request_received"),
        record(0, "response_sent", latency_ms=200, quality_score=0.9, **ok),
        record(0, "request_received"),
        record(0, "response_sent", latency_ms=400, quality_score=0.7, **ok),
        record(1, "request_received"),
        record(1, "request_failed", error_type="RuntimeError", tool_name="retrieval", tool_success=False),
        record(1, "request_received"),
        record(1, "response_sent", latency_ms=3000, quality_score=0.8, **ok),
        record(90, "request_received"),  # ngoài cửa sổ 60 phút
    ]


def test_panels_follow_dashboard_contract_formulas() -> None:
    panels = compute_panels(sample_records(), START, 60)

    assert panels["traffic"]["summary"] == {"count": 4, "rate_per_minute": 0.07}
    assert panels["traffic"]["series"]["requests"][:3] == [2.0, 2.0, 0.0]
    assert panels["latency"]["summary"]["p50"] == 400
    assert panels["latency"]["summary"]["p95"] == 3000
    assert panels["latency"]["summary"]["ttft_p95"] == 50
    assert panels["errors"]["summary"]["error_rate_pct"] == 25.0
    assert panels["errors"]["summary"]["count_by_value"] == {"RuntimeError": 1}
    assert panels["errors"]["summary"]["tool_success_rate_pct"] == 75.0
    assert panels["errors"]["series"]["error_rate_pct"][:3] == [0.0, 50.0, None]
    assert panels["cost"]["summary"]["total"] == 0.006
    assert panels["cost"]["series"]["cumulative"][:2] == [0.004, 0.006]
    assert panels["tokens"]["summary"]["tokens_in"] == 90
    assert panels["tokens"]["summary"]["tokens_out"] == 300
    assert panels["quality"]["summary"]["mean"] == 0.8


def test_threshold_check_uses_contract_aggregation_and_operator() -> None:
    panels = compute_panels(sample_records(), START, 60)

    assert check_threshold(panels["latency"], {"aggregation": "p95", "operator": "lte", "value": 3000}) == (3000, True)
    assert check_threshold(panels["errors"], {"aggregation": "error_rate_pct", "operator": "lte", "value": 2}) == (25.0, False)
    assert check_threshold(panels["quality"], {"aggregation": "mean", "operator": "gte", "value": 0.75}) == (0.8, True)


def test_empty_window_reports_no_data_instead_of_passing() -> None:
    panels = compute_panels([], START, 60)

    assert check_threshold(panels["errors"], {"aggregation": "error_rate_pct", "operator": "lte", "value": 2}) == (None, None)
    assert check_threshold(panels["quality"], {"aggregation": "mean", "operator": "gte", "value": 0.75}) == (None, None)
