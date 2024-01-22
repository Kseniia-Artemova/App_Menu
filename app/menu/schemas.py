from typing import Optional

from pydantic import BaseModel
from uuid import UUID

from app.submenu.schemas import SubmenuReadPydantic


class MenuCreatePydantic(BaseModel):
    title: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class MenuReadPydantic(MenuCreatePydantic):
    submenus_count: int
    submenus: Optional[list[SubmenuReadPydantic]] = None

    class Config:
        from_attributes = True