from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, UUID
from sqlalchemy.orm import relationship
import uuid
from app.database import Base


class Dish(Base):
    __tablename__ = 'dishes'  # Имя таблицы в базе данных

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)  # Уникальный идентификатор блюда
    title = Column(String, index=True)  # Название блюда
    description = Column(String)  # Описание блюда
    price = Column(String)  # Цена блюда

    # Пример связи: предположим, что у каждого блюда есть категория
    submenu_id = Column(UUID, ForeignKey('submenus.id'))  # Внешний ключ на таблицу категорий
    submenu = relationship("Submenu", back_populates="dishes")  # Определяем отношение с моделью категории
