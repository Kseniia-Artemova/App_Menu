from typing import Optional
from pydantic import BaseModel, Field, UUID4, field_validator


class DishCreatePydantic(BaseModel):
    """
    Модель Pydantic для создания блюда

    Проверяет цену на корректность и округляет значение до 2 знаков поле запятой
    """
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
    """
    Модель Pydantic для вывода блюда.
    Содержит все поля, характерные для создания и добавляет вывод id
    """
    id: Optional[UUID4] = None

    class Config:
        from_attributes = True