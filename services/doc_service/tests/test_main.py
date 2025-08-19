import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_generate():
    resp = client.post("/generate", json={"type": "meeting", "source_text": "hello"})
    assert resp.status_code == 200
    assert "hello" in resp.json()["markdown"]
