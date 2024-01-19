from typing import Optional

from pydantic import BaseModel


class DishCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: float

    class Config:
        orm_mode = True
