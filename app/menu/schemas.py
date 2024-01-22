from typing import Optional

from pydantic import BaseModel
from uuid import UUID


class MenuCreate(BaseModel):
    id: Optional[UUID] = None
    title: str
    description: Optional[str] = None

    class Config:
        from_attributes = True