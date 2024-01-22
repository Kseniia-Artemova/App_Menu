from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_async_session
from app.dish.models import Dish
from app.dish.schemas import DishCreate
from app.services import get_submenu_or_404, get_menu_or_404, get_dish_or_404
from app.submenu.models import Submenu

router_dish = APIRouter()


@router_dish.post("/menus/{menu_id}/submenus/{submenu_id}/dishes",
                  response_model=DishCreate, tags=["dishes"], status_code=201)
async def create_dish_for_submenu(menu_id: str,
                                  submenu_id: str,
                                  dish: DishCreate,
                                  db: Session = Depends(get_async_session)):
    await get_menu_or_404(db, menu_id)
    await get_submenu_or_404(db, submenu_id)

    db_dish = Dish(**dish.model_dump(), submenu_id=submenu_id)
    db.add(db_dish)
    await db.commit()
    await db.refresh(db_dish)
    return db_dish


@router_dish.get("/menus/{menu_id}/submenus/{submenu_id}/dishes",
                 response_model=list[DishCreate], tags=["dishes"])
async def read_dishes_for_submenu(menu_id: str,
                                  submenu_id: str,
                                  db: Session = Depends(get_async_session)):
    await get_menu_or_404(db, menu_id)
    await get_submenu_or_404(db, submenu_id)
    return db.query(Dish).filter(Dish.submenu_id == submenu_id).all()


@router_dish.get("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
                 response_model=DishCreate, tags=["dishes"])
async def read_dish_for_submenu(menu_id: str,
                                submenu_id: str,
                                dish_id: str,
                                db: Session = Depends(get_async_session)):
    await get_menu_or_404(db, menu_id)
    await get_submenu_or_404(db, submenu_id)
    dish = await get_dish_or_404(db, dish_id)
    return dish


@router_dish.delete("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
                    tags=["dishes"])
async def delete_dish_for_submenu(menu_id: str,
                                  submenu_id: str,
                                  dish_id: str,
                                  db: Session = Depends(get_async_session)):
    await get_menu_or_404(db, menu_id)
    await get_submenu_or_404(db, submenu_id)
    dish = await get_dish_or_404(db, dish_id)
    await db.delete(dish)
    await db.commit()
    return


@router_dish.patch("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
                   response_model=DishCreate, tags=["dishes"])
async def update_dish_for_submenu(menu_id: str,
                                  submenu_id: str,
                                  dish_id: str,
                                  dish: DishCreate,
                                  db: Session = Depends(get_async_session)):
    await get_menu_or_404(db, menu_id)
    await get_submenu_or_404(db, submenu_id)
    db_dish = await get_dish_or_404(db, dish_id)
    db_dish.title = dish.title
    db_dish.description = dish.description
    db_dish.price = dish.price
    await db.commit()
    await db.refresh(db_dish)
    return db_dish
