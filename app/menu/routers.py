from fastapi import APIRouter, Depends
from sqlalchemy import select, func
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.dish.models import Dish
from app.menu.models import Menu
from app.menu.schemas import MenuCreatePydantic, MenuReadPydantic
from app.services import get_menu_or_404
from app.submenu.models import Submenu

router_menu = APIRouter()


@router_menu.get("/menus", tags=["menus"], response_model=list[MenuReadPydantic])
async def read_menus(db: AsyncSession = Depends(get_async_session)):
    """Эндпойнт для вывода списка меню"""

    menus_result = await db.execute(select(Menu))
    menus = menus_result.scalars().all()

    async def get_menu_info(menu):
        submenus_count_result = await db.execute(
            select(func.count(Submenu.id))
            .where(Submenu.menu_id == menu.id)
        )
        submenus_count = submenus_count_result.scalar_one()

        total_dishes_count_result = await db.execute(
            select(func.count(Dish.id))
            .join(Submenu, Submenu.id == Dish.submenu_id)
            .where(Submenu.menu_id == menu.id)
        )
        total_dishes_count = total_dishes_count_result.scalar_one()

        return MenuReadPydantic(
            id=menu.id,
            title=menu.title,
            description=menu.description,
            submenus_count=submenus_count,
            dishes_count=total_dishes_count
        )

    menus_info = await asyncio.gather(*[get_menu_info(menu) for menu in menus])
    return menus_info


@router_menu.get("/menus/{menu_id}", tags=["menus"], response_model=MenuReadPydantic)
async def read_menu(menu_id: str, db: AsyncSession = Depends(get_async_session)):
    """Эндпойнт для вывода информации о конкретном меню"""

    menu = await get_menu_or_404(db, menu_id)

    submenus_count_result = await db.execute(
        select(func.count(Submenu.id))
        .where(Submenu.menu_id == menu_id)
    )
    submenus_count = submenus_count_result.scalar_one()

    total_dishes_count_result = await db.execute(
        select(func.count(Dish.id))
        .join(Submenu, Submenu.id == Dish.submenu_id)
        .where(Submenu.menu_id == menu_id)
    )
    total_dishes_count = total_dishes_count_result.scalar_one()

    return MenuReadPydantic(
        id=menu.id,
        title=menu.title,
        description=menu.description,
        submenus_count=submenus_count,
        dishes_count=total_dishes_count
    )


@router_menu.post("/menus", tags=["menus"], response_model=MenuReadPydantic, status_code=201)
async def create_menu(menu: MenuCreatePydantic, db: AsyncSession = Depends(get_async_session)):
    """Эндпойнт для создания нового меню"""

    db_menu = Menu(**menu.model_dump())
    db.add(db_menu)
    await db.commit()
    await db.refresh(db_menu)
    return db_menu


@router_menu.patch("/menus/{menu_id}", tags=["menus"], response_model=MenuReadPydantic)
async def update_menu(menu_id: str, menu: MenuCreatePydantic, db: AsyncSession = Depends(get_async_session)):
    """Эндпойнт для обновления информации о конкретном меню"""

    db_menu = await get_menu_or_404(db, menu_id)
    db_menu.title = menu.title
    db_menu.description = menu.description
    await db.commit()
    await db.refresh(db_menu)
    return db_menu


@router_menu.delete("/menus/{menu_id}", tags=["menus"])
async def delete_menu(menu_id: str, db: AsyncSession = Depends(get_async_session)):
    """Эндпойнт для удаления конкретного меню"""

    db_menu = await get_menu_or_404(db, menu_id)
    await db.delete(db_menu)
    await db.commit()

