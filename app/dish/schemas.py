from typing import Optional
from pydantic import BaseModel, model_validator, constr, Field, UUID4
import re


class DishCreatePydantic(BaseModel):
    id: Optional[UUID4] = None
    title: str
    description: Optional[str] = None
    price: str = Field(pattern=r'^\d+\.\d{2}$')

    class Config:
        from_attributes = True


class DishReadPydantic(DishCreatePydantic):

    class Config:
        from_attributes = True