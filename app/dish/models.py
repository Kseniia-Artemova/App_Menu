from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from app.database import Base


class Dish(Base):
    __tablename__ = 'dishes'  # Имя таблицы в базе данных

    id = Column(Integer, primary_key=True, index=True)  # Уникальный идентификатор блюда
    title = Column(String, index=True)  # Название блюда
    description = Column(String)  # Описание блюда
    price = Column(Numeric(10, 2))  # Цена блюда

    # Пример связи: предположим, что у каждого блюда есть категория
    submenu_id = Column(Integer, ForeignKey('submenus.id'))  # Внешний ключ на таблицу категорий
    submenu = relationship("Submenu", back_populates="dishes")  # Определяем отношение с моделью категории
