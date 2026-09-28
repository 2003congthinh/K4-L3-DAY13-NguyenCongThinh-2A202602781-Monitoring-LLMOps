from __future__ import annotations

import sys
from typing import TextIO


def _use_utf8(stream: TextIO) -> None:
    reconfigure = getattr(stream, "reconfigure", None)
    if callable(reconfigure):
        reconfigure(encoding="utf-8", errors="replace")


def configure_utf8_stdio() -> None:
    _use_utf8(sys.stdout)
    _use_utf8(sys.stderr)
