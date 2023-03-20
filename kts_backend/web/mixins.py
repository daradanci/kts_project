from aiohttp.abc import StreamResponse
from aiohttp.web_exceptions import HTTPUnauthorized, HTTPForbidden
from typing import (
    Awaitable,
    Callable,
)
from aiohttp import hdrs


class AuthRequiredMixin:
    async def _iter(self) -> StreamResponse:
        if not getattr(self.request, "admin", None):
            raise HTTPUnauthorized
        return await super(AuthRequiredMixin, self)._iter()
