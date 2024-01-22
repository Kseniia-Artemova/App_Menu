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
    result = await db.execute(select(Menu))
    menus = result.scalars().all()

    async def get_submenu_info_for_menu(menu):
        submenus_result = await db.execute(
            select(Submenu.id, Submenu.title)
            .where(Submenu.menu_id == menu.id)
        )
        submenus = submenus_result.all()

        submenus_with_dish_count = []
        for submenu_id, title in submenus:
            dish_count_result = await db.execute(
                select(func.count(Dish.id))
                .where(Dish.submenu_id == submenu_id)
            )
            dishes_count = dish_count_result.scalar_one()

            submenus_with_dish_count.append({
                "title": title,
                "dishes_count": dishes_count
            })

        return MenuReadPydantic(
            id=menu.id,
            title=menu.title,
            description=menu.description,
            submenus_count=len(submenus),
            submenus=submenus_with_dish_count
        )

    menus_info = await asyncio.gather(*[get_submenu_info_for_menu(menu) for menu in menus])
    return menus_info


@router_menu.get("/menus/{menu_id}", tags=["menus"], response_model=MenuReadPydantic)
async def read_menu(menu_id: str, db: AsyncSession = Depends(get_async_session)):
    menu = await get_menu_or_404(db, menu_id)

    submenus_result = await db.execute(
        select(Submenu.id, Submenu.title)
        .where(Submenu.menu_id == menu_id)
    )
    submenus = submenus_result.all()

    submenus_with_dish_count = []
    for submenu_id, title in submenus:
        dish_count_result = await db.execute(
            select(func.count(Dish.id))
            .where(Dish.submenu_id == submenu_id)
        )
        dishes_count = dish_count_result.scalar_one()

        submenus_with_dish_count.append({
            "title": title,
            "dishes_count": dishes_count
        })

    return MenuReadPydantic(
        id=menu.id,
        title=menu.title,
        description=menu.description,
        submenus_count=len(submenus),
        submenus=submenus_with_dish_count)


@router_menu.post("/menus", tags=["menus"], response_model=MenuCreatePydantic, status_code=201)
async def create_menu(menu: MenuCreatePydantic, db: AsyncSession = Depends(get_async_session)):
    db_menu = Menu(**menu.model_dump())
    db.add(db_menu)
    await db.commit()
    await db.refresh(db_menu)
    return db_menu


@router_menu.patch("/menus/{menu_id}", tags=["menus"], response_model=MenuCreatePydantic)
async def update_menu(menu_id: str, menu: MenuCreatePydantic, db: AsyncSession = Depends(get_async_session)):
    db_menu = await get_menu_or_404(db, menu_id)
    db_menu.title = menu.title
    db_menu.description = menu.description
    await db.commit()
    await db.refresh(db_menu)
    return db_menu


@router_menu.delete("/menus/{menu_id}", tags=["menus"])
async def delete_menu(menu_id: str, db: AsyncSession = Depends(get_async_session)):
    db_menu = await get_menu_or_404(db, menu_id)
    await db.delete(db_menu)
    await db.commit()

