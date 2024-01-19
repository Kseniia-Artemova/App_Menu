from fastapi import FastAPI
from app.database import engine, Base


# Создание всех таблиц в базе данных (вызывается один раз)
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Инициализация FastAPI приложения
app = FastAPI(title="App menu")

