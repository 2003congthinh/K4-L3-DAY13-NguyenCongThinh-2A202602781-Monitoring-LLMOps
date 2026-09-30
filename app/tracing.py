from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Any

from .pii import scrub_text

try:
    from langfuse import Langfuse, get_client, observe, propagate_attributes

    LANGFUSE_SDK_AVAILABLE = True
except ImportError:  # pragma: no cover - chỉ dùng khi chưa cài requirements
    LANGFUSE_SDK_AVAILABLE = False

    def observe(*args: Any, **kwargs: Any):
        def decorator(func):
            return func

        return decorator

    class _DummyClient:
        def update_current_span(self, **kwargs: Any) -> None:
            return None

        def update_current_generation(self, **kwargs: Any) -> None:
            return None

        def score_current_trace(self, **kwargs: Any) -> None:
            return None

        def flush(self) -> None:
            return None

    def get_client():
        return _DummyClient()

    @contextmanager
    def propagate_attributes(**kwargs: Any):
        yield


def get_langfuse_client():
    return get_client()


def tracing_enabled() -> bool:
    return LANGFUSE_SDK_AVAILABLE and bool(
        os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY")
    )


def mask_pii(*, data: Any, **kwargs: Any) -> Any:
    """Langfuse mask hook: scrub PII from every input/output/metadata value before export."""
    if isinstance(data, str):
        return scrub_text(data)
    if isinstance(data, dict):
        return {key: mask_pii(data=value) for key, value in data.items()}
    if isinstance(data, (list, tuple)):
        return [mask_pii(data=value) for value in data]
    return data


# Khởi tạo client một lần, trước mọi get_client()/@observe, để mask được áp dụng cho toàn bộ trace.
if tracing_enabled():
    Langfuse(mask=mask_pii)
