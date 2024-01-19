from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Submenu(Base):
    __tablename__ = 'submenus'  # Имя таблицы в базе данных

    id = Column(Integer, primary_key=True, index=True)  # Уникальный идентификатор подменю
    title = Column(String, index=True)  # Название подменю
    description = Column(String)

    # Пример связи: предположим, что у каждого блюда есть категория
    menu_id = Column(Integer, ForeignKey('menus.id'))  # Внешний ключ на таблицу категорий
    menu = relationship("Menu", back_populates="submenus")  # Определяем отношение с моделью категории

    dishes = relationship("Dish", back_populates="submenu", cascade="all, delete-orphan")