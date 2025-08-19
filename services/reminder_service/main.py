from datetime import datetime
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Reminder(BaseModel):
    id: int
    chat_id: int
    target: str
    fire_at: datetime
    text: str
    status: str = "pending"


_reminders: List[Reminder] = []


@app.post("/reminders", response_model=Reminder)
async def create(reminder: Reminder):
    _reminders.append(reminder)
    return reminder


@app.get("/reminders", response_model=List[Reminder])
async def list_reminders():
    return _reminders


@app.get("/health")
async def health():
    return {"status": "ok"}
