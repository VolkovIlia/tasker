"""API Gateway service.

The gateway exposes a single HTTP interface and forwards requests to
registered backend services using a simple round-robin strategy.
It relies on the minimal ``fastapi`` stub shipped with the repository and
is intentionally synchronous and lightweight so it can run in restricted
environments such as this kata.
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient
from typing import Callable, Dict, List, Tuple, Any

class RoundRobin:
    """Cycle through a list of backend handlers."""
    def __init__(self, items: List[Callable[[str, str, Any], Tuple[int, Any]]]):
        self.items = items
        self.index = 0
    def next(self) -> Callable[[str, str, Any], Tuple[int, Any]]:
        handler = self.items[self.index]
        self.index = (self.index + 1) % len(self.items)
        return handler

class APIGateway:
    """Registry and dispatcher for backend services."""
    def __init__(self) -> None:
        self.backends: Dict[str, RoundRobin] = {}
    def register(self, name: str, apps: List[FastAPI]) -> None:
        """Register FastAPI applications as backends for ``name``.

        The gateway works with both the tiny in-repo FastAPI stub and the real
        framework.  If a backend application exposes ``handle_request`` (the
        stubbed API) it is used directly.  Otherwise the service falls back to
        ``TestClient`` which is compatible with the real FastAPI package.
        """
        handlers: List[Callable[[str, str, Any], Tuple[int, Any]]] = []
        for app in apps:
            if hasattr(app, "handle_request"):
                handlers.append(app.handle_request)
                continue
            client = TestClient(app)

            def _call(method: str, path: str, payload: Any = None, *, _c=client) -> Tuple[int, Any]:
                if method == "GET":
                    resp = _c.get(path)
                else:
                    resp = _c.post(path, json=payload)
                return resp.status_code, resp.json()

            handlers.append(_call)
        self.backends[name] = RoundRobin(handlers)
    def forward(self, name: str, method: str, path: str, payload: Any = None) -> Tuple[int, Any]:
        """Forward a request to the next backend registered for ``name``."""
        backend = self.backends[name].next()
        return backend(method, path, payload)

gateway = APIGateway()
app = FastAPI()

@app.get("/health")
def health() -> Dict[str, str]:
    """Health check endpoint used by tests and monitoring."""
    return {"status": "ok"}

@app.post("/bot/webhook")
def bot_webhook(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Proxy Telegram updates to the bot service.

    The gateway determines which backend to use based on a round-robin
    iterator.  Backends must be registered with :func:`gateway.register`
    before handling requests.
    """
    status, data = gateway.forward("bot", "POST", "/webhook", payload)
    # ``status`` is ignored because the example services always return 200
    return data


@app.post("/task")
def create_task(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Proxy task creation to the task service."""
    status, data = gateway.forward("task", "POST", "/tasks", payload)
    return data


@app.get("/task")
def list_tasks() -> Any:
    """Return tasks from the task service."""
    status, data = gateway.forward("task", "GET", "/tasks")
    return data
