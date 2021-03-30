from sqlalchemy import Column, Integer, String, DateTime
from .database import Base


class Todo(Base):
    __tablename__ = 'Todo'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    due_to = Column(DateTime)
