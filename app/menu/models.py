from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Menu(Base):
    __tablename__ = 'menus'  # Имя таблицы в базе данных

    id = Column(Integer, primary_key=True, index=True)  # Уникальный идентификатор подменю
    title = Column(String, index=True)  # Название подменю
    description = Column(String)

    submenus = relationship("Submenu", back_populates="menu", cascade="all, delete-orphan")