from typing import Optional
from pydantic import BaseModel, UUID4


class SubmenuCreatePydantic(BaseModel):
    """Модель Pydantic для создания подменю"""

    title: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class SubmenuReadPydantic(SubmenuCreatePydantic):
    """
    Модель Pydantic для вывода подменю.

    При выводе также включает id и количество блюд в подменю.
    """
    id: UUID4
    dishes_count: Optional[int] = None

    class Config:
        from_attributes = True