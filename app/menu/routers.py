from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_async_session
from app.menu.models import Menu
from app.menu.schemas import MenuCreate
from app.services import get_menu_or_404

router_menu = APIRouter()


@router_menu.get("/menus", tags=["menus"], response_model=list[MenuCreate])
async def read_menus(db: Session = Depends(get_async_session)):
    result = await db.execute(select(Menu))
    menus = result.scalars().all()
    return menus


@router_menu.get("/menus/{menu_id}", tags=["menus"], response_model=MenuCreate)
async def read_menu(menu_id: str, db: Session = Depends(get_async_session)):
    return await get_menu_or_404(db, menu_id)


@router_menu.post("/menus", tags=["menus"], response_model=MenuCreate, status_code=201)
async def create_menu(menu: MenuCreate, db: Session = Depends(get_async_session)):
    db_menu = Menu(**menu.model_dump())
    db.add(db_menu)
    await db.commit()
    await db.refresh(db_menu)
    return db_menu


@router_menu.patch("/menus/{menu_id}", tags=["menus"], response_model=MenuCreate)
async def update_menu(menu_id: str, menu: MenuCreate, db: Session = Depends(get_async_session)):
    db_menu = await get_menu_or_404(db, menu_id)
    db_menu.title = menu.title
    db_menu.description = menu.description
    await db.commit()
    await db.refresh(db_menu)
    return db_menu


@router_menu.delete("/menus/{menu_id}", tags=["menus"])
async def delete_menu(menu_id: str, db: Session = Depends(get_async_session)):
    db_menu = await get_menu_or_404(db, menu_id)
    await db.delete(db_menu)
    await db.commit()

