from typing import Optional

from pydantic import BaseModel


class SubmenuCreate(BaseModel):
    title: str
    description: Optional[str] = None

    class Config:
        orm_mode = True