from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = None
    time_periods: int | None = None
    status: TaskStatus = Field(default=TaskStatus.todo)
    category_id: int


class ResponseTask(Task):
    id: int
    user_id: int
