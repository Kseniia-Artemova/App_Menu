from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.dish.models import Dish
from app.services import get_menu_or_404, get_submenu_or_404
from app.submenu.models import Submenu
from app.submenu.schemas import SubmenuCreatePydantic, SubmenuReadPydantic

router_submenu = APIRouter()


@router_submenu.get("/menus/{menu_id}/submenus", response_model=list[SubmenuReadPydantic], tags=["submenus"])
async def read_submenus_for_menu(menu_id: str, db: AsyncSession = Depends(get_async_session)):
    """Эндпойнт для получения списка подменю для конкретного меню"""

    await get_menu_or_404(db, menu_id)
    result = await db.execute(
        select(Submenu, func.count(Dish.id).label("dishes_count"))
        .join(Dish, isouter=True)
        .group_by(Submenu.id)
        .filter(Submenu.menu_id == menu_id)
    )
    submenus_with_counts = result.all()
    return [
        SubmenuReadPydantic(
            id=submenu.id,
            title=submenu.title,
            description=submenu.description,
            dishes_count=dishes_count
        ) for submenu, dishes_count in submenus_with_counts
    ]


@router_submenu.post("/menus/{menu_id}/submenus",
                     response_model=SubmenuReadPydantic, tags=["submenus"], status_code=201)
async def create_submenu_for_menu(menu_id: str,
                                  submenu: SubmenuCreatePydantic,
                                  db: AsyncSession = Depends(get_async_session)):
    """Эндпойнт для создания подменю"""

    await get_menu_or_404(db, menu_id)
    db_submenu = Submenu(**submenu.model_dump(), menu_id=menu_id)
    db.add(db_submenu)
    await db.commit()
    await db.refresh(db_submenu)
    return db_submenu


@router_submenu.get("/menus/{menu_id}/submenus/{submenu_id}",
                    response_model=SubmenuReadPydantic, tags=["submenus"])
async def read_submenu_for_menu(menu_id: str,
                                submenu_id: str,
                                db: AsyncSession = Depends(get_async_session)):
    """Эндпойнт для вывода конкретного подменю"""

    await get_menu_or_404(db, menu_id)
    result = await db.execute(
        select(Submenu, func.count(Dish.id).label("dishes_count"))
        .join(Dish, isouter=True)
        .group_by(Submenu.id)
        .filter(Submenu.id == submenu_id)
    )
    submenu_with_count = result.first()

    if not submenu_with_count:
        raise HTTPException(status_code=404, detail="submenu not found")

    submenu, dishes_count = submenu_with_count
    return SubmenuReadPydantic(
        id=submenu.id,
        title=submenu.title,
        description=submenu.description,
        dishes_count=dishes_count
    )


@router_submenu.patch("/menus/{menu_id}/submenus/{submenu_id}",
                      response_model=SubmenuReadPydantic, tags=["submenus"])
async def update_submenu_for_menu(menu_id: str,
                                  submenu_id: str,
                                  submenu: SubmenuCreatePydantic,
                                  db: AsyncSession = Depends(get_async_session)):
    """Эндпойнт для обновления информации о конкретном подменю"""

    await get_menu_or_404(db, menu_id)
    db_submenu = await get_submenu_or_404(db, submenu_id)
    db_submenu.title = submenu.title
    db_submenu.description = submenu.description
    await db.commit()
    await db.refresh(db_submenu)
    return db_submenu


@router_submenu.delete("/menus/{menu_id}/submenus/{submenu_id}",
                       tags=["submenus"], status_code=200)
async def delete_submenu_for_menu(menu_id: str,
                                  submenu_id: str,
                                  db: AsyncSession = Depends(get_async_session)):
    """Эндпойнт для удаления подменю"""

    await get_menu_or_404(db, menu_id)
    db_submenu = await get_submenu_or_404(db, submenu_id)
    await db.delete(db_submenu)
    await db.commit()
    return
