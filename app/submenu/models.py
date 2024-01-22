from sqlalchemy import Column, String, ForeignKey, UUID
from sqlalchemy.orm import relationship
import uuid
from app.database import Base


class Submenu(Base):
    """Модель подменю"""

    __tablename__ = 'submenus'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, index=True)
    description = Column(String)

    menu_id = Column(UUID, ForeignKey('menus.id'))
    menu = relationship("Menu", back_populates="submenus")

    dishes = relationship("Dish", back_populates="submenu", cascade="all, delete-orphan")