from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.dish.models import Dish
from app.menu.models import Menu
from app.submenu.models import Submenu


async def get_menu_or_404(db: AsyncSession, menu_id: str) -> Menu:
    menu = await db.get(Menu, menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")
    return menu


async def get_submenu_or_404(db: AsyncSession, submenu_id: str) -> Submenu:
    submenu = await db.get(Submenu, submenu_id)
    if not submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    return submenu


async def get_dish_or_404(db: AsyncSession, dish_id: str) -> Dish:
    dish = await db.get(Dish, dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="dish not found")
    return dish