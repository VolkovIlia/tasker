from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx
import os
import itertools

app = FastAPI()

_task_backends = itertools.cycle(os.getenv("TASK_SERVICE_URLS", "http://task-service:8000").split(","))
_doc_backends = itertools.cycle(os.getenv("DOC_SERVICE_URLS", "http://doc-service:8000").split(","))
_reminder_backends = itertools.cycle(os.getenv("REMINDER_SERVICE_URLS", "http://reminder-service:8000").split(","))
_bot_backends = itertools.cycle(os.getenv("BOT_SERVICE_URLS", "http://bot:8000").split(","))

async def _forward(request: Request, url: str) -> JSONResponse:
    data = await request.body()
    headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}
    async with httpx.AsyncClient() as client:
        resp = await client.request(request.method, url, content=data, headers=headers, params=request.query_params)
    content = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else resp.text
    return JSONResponse(status_code=resp.status_code, content=content)

@app.api_route("/tasks", methods=["GET", "POST"])
async def tasks(request: Request):
    backend = next(_task_backends)
    return await _forward(request, f"{backend}/tasks")

@app.api_route("/reminders", methods=["GET", "POST"])
async def reminders(request: Request):
    backend = next(_reminder_backends)
    return await _forward(request, f"{backend}/reminders")

@app.post("/docs/generate")
async def docs_generate(request: Request):
    backend = next(_doc_backends)
    return await _forward(request, f"{backend}/generate")

@app.post("/bot/webhook")
async def bot_webhook(request: Request):
    backend = next(_bot_backends)
    return await _forward(request, f"{backend}/webhook")

@app.get("/health")
async def health():
    return {"status": "ok"}
