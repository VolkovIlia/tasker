"""A tiny stub of the :mod:`fastapi` package used for offline tests.

This module provides a minimal subset of FastAPI's interface so that the
example services can be exercised without installing external dependencies.
It supports registering synchronous GET and POST routes and exposes a
``FastAPI`` application object with a :py:meth:`handle_request` method used by
unit tests and the API gateway.
"""

from typing import Any, Callable, Dict, Tuple

class HTTPException(Exception):
    """Lightweight HTTP exception carrying a status code and detail message."""

    def __init__(self, status_code: int, detail: str) -> None:
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail

class FastAPI:
    """Very small web framework inspired by FastAPI.

    Only the features required for the unit tests are implemented:

    * Route registration via :py:meth:`get` and :py:meth:`post` decorators.
    * A :py:meth:`handle_request` helper that dispatches a request to the
      registered handler and returns ``(status_code, payload)``.
    """

    def __init__(self) -> None:
        self._routes: Dict[str, Dict[str, Callable[[Any], Any]]] = {
            "GET": {},
            "POST": {},
        }

    def get(self, path: str) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
        """Register a synchronous GET endpoint."""
        def decorator(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
            self._routes["GET"][path] = func
            return func
        return decorator

    def post(self, path: str) -> Callable[[Callable[[Any], Any]], Callable[[Any], Any]]:
        """Register a synchronous POST endpoint."""
        def decorator(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
            self._routes["POST"][path] = func
            return func
        return decorator

    def handle_request(self, method: str, path: str, json: Any = None) -> Tuple[int, Any]:
        """Dispatch the request to the registered handler.

        Parameters
        ----------
        method:
            HTTP verb in upper case (e.g. ``"GET"`` or ``"POST"``).
        path:
            Request path starting with ``/``.
        json:
            Parsed JSON payload supplied for POST requests.
        """
        handler = self._routes.get(method, {}).get(path)
        if handler is None:
            return 404, {"detail": "Not Found"}
        if json is None:
            return 200, handler()
        return 200, handler(json)

__all__ = ["FastAPI", "HTTPException"]
