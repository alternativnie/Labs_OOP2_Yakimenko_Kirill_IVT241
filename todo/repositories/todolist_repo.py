# repositories/todolist_repo.py
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from models import TodoList
from schemas import TodoListCreate, TodoListUpdate


class TodoListRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: TodoListCreate) -> TodoList:
        todolist = TodoList(name=data.name)
        self.session.add(todolist)
        await self.session.commit()
        await self.session.refresh(todolist)
        return todolist

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[TodoList]:
        result = await self.session.execute(
            select(TodoList).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_by_id(self, todolist_id: int) -> Optional[TodoList]:
        result = await self.session.execute(
            select(TodoList).where(TodoList.id == todolist_id)
        )
        return result.scalar_one_or_none()

    async def get_with_items(self, todolist_id: int) -> Optional[TodoList]:
        from sqlalchemy.orm import selectinload

        result = await self.session.execute(
            select(TodoList)
            .where(TodoList.id == todolist_id)
            .options(selectinload(TodoList.items))
        )
        return result.scalar_one_or_none()

    async def update(self, todolist_id: int, data: TodoListUpdate) -> Optional[TodoList]:
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get_by_id(todolist_id)

        await self.session.execute(
            update(TodoList)
            .where(TodoList.id == todolist_id)
            .values(**update_data)
        )
        await self.session.commit()
        return await self.get_by_id(todolist_id)

    async def delete(self, todolist_id: int) -> bool:
        result = await self.session.execute(
            delete(TodoList).where(TodoList.id == todolist_id)
        )
        await self.session.commit()
        return result.rowcount > 0