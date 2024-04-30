from pydantic import BaseModel, Field, model_validator


class Task(BaseModel):
    name: str | None = None
    time_periods: int | None = None
    category_id: int


class ResponseTask(Task):
    id: int