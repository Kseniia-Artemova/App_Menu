from fastapi import FastAPI
from app.database import engine, Base
from app.dish.routers import router_dish
from app.menu.routers import router_menu
from app.submenu.routers import router_submenu


async def create_tables():
    """Создание всех таблиц в базе данных (вызывается один раз)"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Инициализация FastAPI приложения
app = FastAPI(title="App menu")

app.include_router(router_dish, prefix="/api/v1")
app.include_router(router_submenu, prefix="/api/v1")
app.include_router(router_menu, prefix="/api/v1")

