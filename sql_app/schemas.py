from typing import List, Optional

from pydantic import BaseModel


class TaskBase(BaseModel):
    cert_type: str
    full_name: str
    student_id: int

class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True
