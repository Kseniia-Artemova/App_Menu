from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.dish.models import Dish
from app.dish.schemas import DishCreatePydantic, DishReadPydantic
from app.services import get_submenu_or_404, get_menu_or_404, get_dish_or_404

router_dish = APIRouter()


@router_dish.post("/menus/{menu_id}/submenus/{submenu_id}/dishes",
                  response_model=DishReadPydantic, tags=["dishes"], status_code=201)
async def create_dish_for_submenu(menu_id: str,
                                  submenu_id: str,
                                  dish: DishCreatePydantic,
                                  db: AsyncSession = Depends(get_async_session)):
    """Эндпойнт для создания блюда"""

    await get_menu_or_404(db, menu_id)
    await get_submenu_or_404(db, submenu_id)

    db_dish = Dish(**dish.model_dump(), submenu_id=submenu_id)
    db.add(db_dish)
    await db.commit()
    await db.refresh(db_dish)
    return db_dish


@router_dish.get("/menus/{menu_id}/submenus/{submenu_id}/dishes",
                 response_model=list[DishReadPydantic], tags=["dishes"])
async def read_dishes_for_submenu(menu_id: str,
                                  submenu_id: str,
                                  db: AsyncSession = Depends(get_async_session)):
    """Эндпойнт для вывода списка блюд конкретного подменю"""

    result = await db.execute(select(Dish).filter(Dish.submenu_id == submenu_id))
    dishes = result.scalars().all()
    return dishes


@router_dish.get("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
                 response_model=DishReadPydantic, tags=["dishes"])
async def read_dish_for_submenu(menu_id: str,
                                submenu_id: str,
                                dish_id: str,
                                db: AsyncSession = Depends(get_async_session)):
    """Эндпойнт для вывода конкретного блюда"""

    await get_menu_or_404(db, menu_id)
    await get_submenu_or_404(db, submenu_id)
    dish = await get_dish_or_404(db, dish_id)
    return dish


@router_dish.delete("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
                    tags=["dishes"], status_code=200)
async def delete_dish_for_submenu(menu_id: str,
                                  submenu_id: str,
                                  dish_id: str,
                                  db: AsyncSession = Depends(get_async_session)):
    """Эндпойнт для удаления блюда"""

    await get_menu_or_404(db, menu_id)
    await get_submenu_or_404(db, submenu_id)
    dish = await get_dish_or_404(db, dish_id)
    await db.delete(dish)
    await db.commit()
    return


@router_dish.patch("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
                   response_model=DishReadPydantic, tags=["dishes"])
async def update_dish_for_submenu(menu_id: str,
                                  submenu_id: str,
                                  dish_id: str,
                                  dish: DishCreatePydantic,
                                  db: AsyncSession = Depends(get_async_session)):
    """Эндпойнт для обновления информации о конкретном блюде"""

    await get_menu_or_404(db, menu_id)
    await get_submenu_or_404(db, submenu_id)
    db_dish = await get_dish_or_404(db, dish_id)
    db_dish.title = dish.title
    db_dish.description = dish.description
    db_dish.price = dish.price
    await db.commit()
    await db.refresh(db_dish)
    return db_dish
