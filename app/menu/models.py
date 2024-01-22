from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship
import uuid
from app.database import Base


class Menu(Base):
    __tablename__ = 'menus'  # Имя таблицы в базе данных

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)  # Уникальный идентификатор подменю
    title = Column(String, index=True)  # Название подменю
    description = Column(String)

    submenus = relationship("Submenu", back_populates="menu", cascade="all, delete-orphan")