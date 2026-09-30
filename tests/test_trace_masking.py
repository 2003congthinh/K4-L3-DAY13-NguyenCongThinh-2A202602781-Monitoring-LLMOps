from __future__ import annotations

from app.tracing import mask_pii


def test_mask_pii_scrubs_nested_trace_payloads() -> None:
    masked = mask_pii(
        data={
            "query_preview": "Contact a@example.com or 0912345678",
            "documents": ["CCCD 012345678901"],
            "doc_count": 1,
        }
    )

    assert masked == {
        "query_preview": "Contact [REDACTED_EMAIL] or [REDACTED_PHONE_VN]",
        "documents": ["CCCD [REDACTED_CCCD]"],
        "doc_count": 1,
    }
