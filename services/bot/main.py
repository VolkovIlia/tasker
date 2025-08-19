from fastapi import FastAPI, Request
import httpx

app = FastAPI()

TASK_SERVICE_URL = "http://task-service:8000"
DOC_SERVICE_URL = "http://doc-service:8000"

@app.post("/webhook")
async def telegram_webhook(request: Request):
    payload = await request.json()
    # TODO: parse Telegram update and route command
    return {"ok": True, "received": payload}

@app.get("/health")
async def health():
    return {"status": "ok"}
