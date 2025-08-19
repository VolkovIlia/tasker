from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class Task(BaseModel):
    id: int
    chat_id: int
    message_id: int
    title: str
    description: Optional[str] = None
    assignee: Optional[str] = None
    due_at: Optional[datetime] = None
    status: str = "todo"
    tags: List[str] = Field(default_factory=list)
    created_by: str
    created_at: datetime
    updated_at: datetime
