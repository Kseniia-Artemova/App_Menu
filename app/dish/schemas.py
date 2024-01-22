from typing import Optional
from pydantic import BaseModel, model_validator, Field, UUID4, field_validator


class DishCreatePydantic(BaseModel):
    id: Optional[UUID4] = None
    title: str
    description: Optional[str] = None
    price: str = Field(pattern=r'^\d+\.\d{2}$')

    @field_validator('price', mode='before')
    @classmethod
    def validate_and_format_price(cls, value):
        try:
            price_float = round(float(value), 2)
            return f"{price_float:.2f}"
        except ValueError:
            raise ValueError("Price must be a valid number")

    class Config:
        from_attributes = True


class DishReadPydantic(DishCreatePydantic):

    class Config:
        from_attributes = True