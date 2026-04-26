# bootstrap.py
from fastapi import FastAPI

from endpoints import todolist_endpoints, item_endpoints


def bootstrap(app: FastAPI) -> None:

    # Инициализируем роуты для TodoList
    todolist_endpoints.init_routes(app)

    # Инициализируем роуты для Item
    item_endpoints.init_routes(app)

    print("✅ Все роуты зарегистрированы")