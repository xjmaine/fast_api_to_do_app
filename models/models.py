# from email.policy import default
from sqlalchemy import Boolean, Column, Integer, String
from databases.database import Base
from sqlalchemy.sql.expression import false


class Todo(Base):
    __tablename__ = 'todos'
    id=Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    complete = Column(Boolean, default=false())
    