# repositories/item_repo.py
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from models import Item
from schemas import ItemCreate, ItemUpdate


class ItemRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, todolist_id: int, data: ItemCreate) -> Optional[Item]:
        # Проверяем, существует ли TodoList
        from repositories.todolist_repo import TodoListRepository
        todolist_repo = TodoListRepository(self.session)
        todolist = await todolist_repo.get_by_id(todolist_id)

        if not todolist:
            return None

        item = Item(
            name=data.name,
            text=data.text,
            is_done=data.is_done,
            todolist_id=todolist_id
        )
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def get_all(self, todolist_id: int, skip: int = 0, limit: int = 100) -> List[Item]:
        """Получить все элементы из списка"""
        result = await self.session.execute(
            select(Item)
            .where(Item.todolist_id == todolist_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_id(self, item_id: int) -> Optional[Item]:
        result = await self.session.execute(
            select(Item).where(Item.id == item_id)
        )
        return result.scalar_one_or_none()

    async def update(self, item_id: int, data: ItemUpdate) -> Optional[Item]:
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get_by_id(item_id)

        await self.session.execute(
            update(Item)
            .where(Item.id == item_id)
            .values(**update_data)
        )
        await self.session.commit()
        return await self.get_by_id(item_id)

    async def delete(self, item_id: int) -> bool:
        result = await self.session.execute(
            delete(Item).where(Item.id == item_id)
        )
        await self.session.commit()
        return result.rowcount > 0