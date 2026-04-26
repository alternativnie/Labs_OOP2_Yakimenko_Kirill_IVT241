
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from database import create_tables
from bootstrap import bootstrap


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Запуск приложения...")
    await create_tables()  # Создаём таблицы при старте
    print("✅ Таблицы созданы")
    yield
    print("👋 Остановка приложения...")


def create_app() -> FastAPI:
    app = FastAPI(
        title="TodoList API",
        description="API для управления списками дел",
        version="1.0.0",
        lifespan=lifespan
    )

    bootstrap(app)
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # автоматическая перезагрузка при изменениях
    )