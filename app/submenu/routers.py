from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_async_session
from app.services import get_menu_or_404, get_submenu_or_404
from app.submenu.models import Submenu
from app.submenu.schemas import SubmenuCreate

router_submenu = APIRouter()


@router_submenu.get("/menus/{menu_id}/submenus",
                    response_model=list[SubmenuCreate], tags=["submenus"])
async def read_submenus_for_menu(menu_id: str,
                                 db: Session = Depends(get_async_session)):
    await get_menu_or_404(db, menu_id)
    return db.query(Submenu).filter(Submenu.menu_id == menu_id).all()


@router_submenu.post("/menus/{menu_id}/submenus",
                     response_model=SubmenuCreate, tags=["submenus"], status_code=201)
async def create_submenu_for_menu(menu_id: str,
                                  submenu: SubmenuCreate,
                                  db: Session = Depends(get_async_session)):
    await get_menu_or_404(db, menu_id)
    db_submenu = Submenu(**submenu.model_dump(), menu_id=menu_id)
    db.add(db_submenu)
    await db.commit()
    await db.refresh(db_submenu)
    return db_submenu


@router_submenu.get("/menus/{menu_id}/submenus/{submenu_id}",
                    response_model=SubmenuCreate, tags=["submenus"])
async def read_submenu_for_menu(menu_id: str,
                                submenu_id: str,
                                db: Session = Depends(get_async_session)):
    await get_menu_or_404(db, menu_id)
    db_submenu = await get_submenu_or_404(db, submenu_id)
    return db_submenu


@router_submenu.patch("/menus/{menu_uuid}/submenus/{submenu_uuid}",
                      response_model=SubmenuCreate, tags=["submenus"])
async def update_submenu_for_menu(menu_id: str,
                                  submenu_id: str,
                                  submenu: SubmenuCreate,
                                  db: Session = Depends(get_async_session)):
    await get_menu_or_404(db, menu_id)
    db_submenu = await get_submenu_or_404(db, submenu_id)
    db_submenu.title = submenu.title
    db_submenu.description = submenu.description
    await db.commit()
    await db.refresh(db_submenu)
    return db_submenu


@router_submenu.delete("/menus/{menu_id}/submenus/{submenu_id}",
                       tags=["submenus"])
async def delete_submenu_for_menu(menu_id: str,
                                  submenu_id: str,
                                  db: Session = Depends(get_async_session)):
    await get_menu_or_404(db, menu_id)
    db_submenu = await get_submenu_or_404(db, submenu_id)
    await db.delete(db_submenu)
    await db.commit()
    return
