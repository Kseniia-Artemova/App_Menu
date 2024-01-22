from typing import Optional

from pydantic import BaseModel, UUID4


class SubmenuCreatePydantic(BaseModel):
    id: Optional[UUID4] = None
    title: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class SubmenuReadPydantic(SubmenuCreatePydantic):
    dishes_count: int

    class Config:
        from_attributes = True