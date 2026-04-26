# schemas.py
from pydantic import BaseModel, Field
from typing import Optional



class TodoListCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)


class TodoListUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)


class TodoListResponse(BaseModel):

    id: int
    name: str

    class Config:
        from_attributes = True  # для Pydantic v2


class TodoListWithItemsResponse(BaseModel):

    id: int
    name: str
    items: list["ItemResponse"] = []

    class Config:
        from_attributes = True




class ItemCreate(BaseModel):

    name: str = Field(..., min_length=1, max_length=200)
    text: Optional[str] = None
    is_done: bool = False


class ItemUpdate(BaseModel):

    name: Optional[str] = Field(None, min_length=1, max_length=200)
    text: Optional[str] = None
    is_done: Optional[bool] = None


class ItemResponse(BaseModel):

    id: int
    name: str
    text: Optional[str] = None
    is_done: bool
    todolist_id: int

    class Config:
        from_attributes = True



TodoListWithItemsResponse.model_rebuild()