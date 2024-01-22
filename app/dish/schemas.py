from typing import Optional
from pydantic import BaseModel, model_validator, constr, Field
import re


class DishCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: str = Field(pattern=r'^\d+\.\d{2}$')

    class Config:
        from_attributes = True
