"""In-memory Task service implemented with the FastAPI stub.

The service exposes two endpoints:

* ``POST /tasks`` — create a new task.
* ``GET /tasks`` — return the list of existing tasks.

The real project would persist tasks in a database but for the purposes
of this kata everything is stored in a simple Python list.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException

app = FastAPI()

# In-memory store of tasks.
TASKS: List[Dict[str, Any]] = []
_task_counter = 1


@app.post("/tasks")
def create_task(data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new task and return it.

    Parameters
    ----------
    data:
        JSON payload containing at minimum ``title`` and ``chat_id``.
    """
    global _task_counter
    title = data.get("title")
    chat_id = data.get("chat_id")
    if not title or not chat_id:
        raise HTTPException(400, "title and chat_id are required")

    task = {
        "id": _task_counter,
        "chat_id": chat_id,
        "title": title,
        "assignee": data.get("assignee"),
        "due_at": data.get("due_at"),
        "tags": data.get("tags", []),
        "created_at": datetime.utcnow().isoformat(),
    }
    TASKS.append(task)
    _task_counter += 1
    return task


@app.get("/tasks")
def list_tasks() -> List[Dict[str, Any]]:
    """Return all stored tasks."""
    return TASKS


if __name__ == "__main__":
    # Allow running ``python main.py`` for manual exploration.
    import json
    print(json.dumps(list_tasks(), indent=2))
