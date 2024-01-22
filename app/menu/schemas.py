from typing import Optional
from pydantic import BaseModel
from uuid import UUID


class MenuCreatePydantic(BaseModel):
    """Модель Pydantic для создания меню"""

    title: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class MenuReadPydantic(MenuCreatePydantic):
    """
    Модель Pydantic для вывода меню.

    Содержит те же поля, что и при создании,
    добавляет поля для вывода id и количество подменю и блюд.
    """

    id: UUID
    submenus_count: Optional[int] = None
    dishes_count: Optional[int] = None

    class Config:
        from_attributes = True