"""Testing helpers for the :mod:`fastapi` stub.

The real FastAPI library ships with a starlette-based ``TestClient`` that
spins up the ASGI application.  For the purposes of these exercises we simply
call :py:meth:`fastapi.FastAPI.handle_request` directly.
"""

from typing import Any
from . import FastAPI

class Response:
    """Minimal response object mimicking ``requests.Response``."""
    def __init__(self, status_code: int, data: Any) -> None:
        self.status_code = status_code
        self._data = data
    def json(self) -> Any:
        return self._data

class TestClient:
    """Synchronous test client for the stubbed :class:`FastAPI` apps."""
    def __init__(self, app: FastAPI) -> None:
        self.app = app
    def get(self, path: str) -> Response:
        status, data = self.app.handle_request("GET", path)
        return Response(status, data)
    def post(self, path: str, json: Any = None) -> Response:
        status, data = self.app.handle_request("POST", path, json)
        return Response(status, data)
