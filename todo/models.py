# models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base


class TodoList(Base):
    __tablename__ = "todolists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)

    # Связь с Item (один ко многим)
    items = relationship("Item", back_populates="todolist", cascade="all, delete-orphan")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    text = Column(Text, nullable=True)
    is_done = Column(Boolean, default=False)

    # Внешний ключ на TodoList
    todolist_id = Column(Integer, ForeignKey("todolists.id", ondelete="CASCADE"))

    # Связь с TodoList
    todolist = relationship("TodoList", back_populates="items")