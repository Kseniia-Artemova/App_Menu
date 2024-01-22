from typing import Optional

from pydantic import BaseModel


class SubmenuCreatePydantic(BaseModel):
    title: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class SubmenuReadPydantic(SubmenuCreatePydantic):
    dish_count: int

    class Config:
        from_attributes = True