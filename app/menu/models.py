from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship
import uuid
from app.database import Base


class Menu(Base):
    """Модель меню"""

    __tablename__ = 'menus'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, index=True)
    description = Column(String)

    submenus = relationship("Submenu", back_populates="menu", cascade="all, delete-orphan")