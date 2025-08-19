import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient
from main import app
import httpx

client = TestClient(app)

async def _mock_request(self, method, url, **kwargs):
    return httpx.Response(200, json={"proxied": url})

def test_tasks_forward(monkeypatch):
    monkeypatch.setattr(httpx.AsyncClient, "request", _mock_request)
    resp = client.get("/tasks")
    assert resp.status_code == 200
    assert resp.json()["proxied"].endswith("/tasks")
