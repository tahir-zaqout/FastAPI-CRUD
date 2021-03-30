from pydantic import BaseModel
from fastapi import Form


class Todo(BaseModel):
    name: str
    description: str
