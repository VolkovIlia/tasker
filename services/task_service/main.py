from fastapi import FastAPI
from typing import List
from models import Task

app = FastAPI()

_tasks: List[Task] = []

@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    _tasks.append(task)
    return task

@app.get("/tasks", response_model=List[Task])
async def list_tasks():
    return _tasks

@app.get("/health")
async def health():
    return {"status": "ok"}
