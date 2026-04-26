
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database import get_db
from repositories.item_repo import ItemRepository
from schemas import ItemCreate, ItemUpdate, ItemResponse


class ItemEndpoints:

    async def create_item(
            self,
            todolist_id: int,
            data: ItemCreate,
            session: AsyncSession = Depends(get_db)
    ) -> ItemResponse:
        repo = ItemRepository(session)
        item = await repo.create(todolist_id, data)

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="TodoList not found"
            )

        return ItemResponse.model_validate(item)

    async def get_all_items(
            self,
            todolist_id: int,
            skip: int = 0,
            limit: int = 100,
            session: AsyncSession = Depends(get_db)
    ) -> List[ItemResponse]:
        repo = ItemRepository(session)
        items = await repo.get_all(todolist_id, skip, limit)
        return [ItemResponse.model_validate(i) for i in items]

    async def get_item(
            self,
            item_id: int,
            session: AsyncSession = Depends(get_db)
    ) -> ItemResponse:
        repo = ItemRepository(session)
        item = await repo.get_by_id(item_id)

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )

        return ItemResponse.model_validate(item)

    async def update_item(
            self,
            item_id: int,
            data: ItemUpdate,
            session: AsyncSession = Depends(get_db)
    ) -> ItemResponse:
        repo = ItemRepository(session)
        item = await repo.update(item_id, data)

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )

        return ItemResponse.model_validate(item)

    async def delete_item(
            self,
            item_id: int,
            session: AsyncSession = Depends(get_db)
    ) -> dict:
        repo = ItemRepository(session)
        deleted = await repo.delete(item_id)

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )

        return {"message": "Item deleted successfully"}


def init_routes(app: FastAPI) -> None:
    endpoints = ItemEndpoints()

    app.add_api_route(
        path="/todolists/{todolist_id}/items",
        endpoint=endpoints.create_item,
        methods=["POST"],
        response_model=ItemResponse,
        status_code=status.HTTP_201_CREATED
    )

    app.add_api_route(
        path="/todolists/{todolist_id}/items",
        endpoint=endpoints.get_all_items,
        methods=["GET"],
        response_model=List[ItemResponse]
    )


    app.add_api_route(
        path="/items/{item_id}",
        endpoint=endpoints.get_item,
        methods=["GET"],
        response_model=ItemResponse
    )

    app.add_api_route(
        path="/items/{item_id}",
        endpoint=endpoints.update_item,
        methods=["PUT"],
        response_model=ItemResponse
    )

    app.add_api_route(
        path="/items/{item_id}",
        endpoint=endpoints.delete_item,
        methods=["DELETE"]
    )