from __future__ import annotations

STATE = {
    "rag_slow": False,
    "tool_fail": False,
    "cost_spike": False,
}


def enable(name: str) -> None:
    if name not in STATE:
        raise KeyError(f"Unknown incident: {name}")
    STATE[name] = True



def disable(name: str) -> None:
    if name not in STATE:
        raise KeyError(f"Unknown incident: {name}")
    STATE[name] = False



def status() -> dict[str, bool]:
    return dict(STATE)
