# endpoints/todolist_endpoints.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database import get_db
from repositories.todolist_repo import TodoListRepository
from schemas import TodoListCreate, TodoListUpdate, TodoListResponse, TodoListWithItemsResponse


class TodoListEndpoints:

    async def create_todolist(
            self,
            data: TodoListCreate,
            session: AsyncSession = Depends(get_db)
    ) -> TodoListResponse:
        repo = TodoListRepository(session)
        todolist = await repo.create(data)
        return TodoListResponse.model_validate(todolist)

    async def get_all_todolists(
            self,
            skip: int = 0,
            limit: int = 100,
            session: AsyncSession = Depends(get_db)
    ) -> List[TodoListResponse]:
        repo = TodoListRepository(session)
        todolists = await repo.get_all(skip, limit)
        return [TodoListResponse.model_validate(t) for t in todolists]

    async def get_todolist(
            self,
            todolist_id: int,
            session: AsyncSession = Depends(get_db)
    ) -> TodoListWithItemsResponse:
        repo = TodoListRepository(session)
        todolist = await repo.get_with_items(todolist_id)

        if not todolist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="TodoList not found"
            )

        return TodoListWithItemsResponse.model_validate(todolist)

    async def update_todolist(
            self,
            todolist_id: int,
            data: TodoListUpdate,
            session: AsyncSession = Depends(get_db)
    ) -> TodoListResponse:
        repo = TodoListRepository(session)
        todolist = await repo.update(todolist_id, data)

        if not todolist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="TodoList not found"
            )

        return TodoListResponse.model_validate(todolist)

    async def delete_todolist(
            self,
            todolist_id: int,
            session: AsyncSession = Depends(get_db)
    ) -> dict:
        repo = TodoListRepository(session)
        deleted = await repo.delete(todolist_id)

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="TodoList not found"
            )

        return {"message": "TodoList deleted successfully"}


def init_routes(app: FastAPI) -> None:
    endpoints = TodoListEndpoints()

    app.add_api_route(
        path="/todolists",
        endpoint=endpoints.create_todolist,
        methods=["POST"],
        response_model=TodoListResponse,
        status_code=status.HTTP_201_CREATED
    )

    app.add_api_route(
        path="/todolists",
        endpoint=endpoints.get_all_todolists,
        methods=["GET"],
        response_model=List[TodoListResponse]
    )

    app.add_api_route(
        path="/todolists/{todolist_id}",
        endpoint=endpoints.get_todolist,
        methods=["GET"],
        response_model=TodoListWithItemsResponse
    )

    app.add_api_route(
        path="/todolists/{todolist_id}",
        endpoint=endpoints.update_todolist,
        methods=["PUT"],
        response_model=TodoListResponse
    )

    app.add_api_route(
        path="/todolists/{todolist_id}",
        endpoint=endpoints.delete_todolist,
        methods=["DELETE"]
    )