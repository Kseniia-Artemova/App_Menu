from typing import Optional

from pydantic import BaseModel, UUID4
from uuid import UUID

from app.submenu.schemas import SubmenuReadPydantic


class MenuCreatePydantic(BaseModel):
    id: Optional[UUID] = None
    title: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class MenuReadPydantic(MenuCreatePydantic):
    submenus_count: int
    dishes_count: int

    class Config:
        from_attributes = True