from __future__ import annotations

import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from structlog.contextvars import bind_contextvars, clear_contextvars


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # TODO: Clear contextvars to avoid leakage between requests
        # clear_contextvars()

        # TODO: Extract x-request-id from headers or generate a new one
        # Use format: req-<8-char-hex>
        correlation_id = "MISSING"
        
        # TODO: Bind the correlation_id to structlog contextvars
        # bind_contextvars(correlation_id=correlation_id)
        
        request.state.correlation_id = correlation_id
        
        start = time.perf_counter()
        response = await call_next(request)
        
        # TODO: Add the correlation_id and processing time to response headers
        # response.headers["x-request-id"] = correlation_id
        # response.headers["x-response-time-ms"] = ...
        
        return response
