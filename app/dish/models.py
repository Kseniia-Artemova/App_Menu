from sqlalchemy import Column, String, ForeignKey, UUID
from sqlalchemy.orm import relationship
import uuid
from app.database import Base


class Dish(Base):
    """Модель блюда"""

    __tablename__ = 'dishes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, index=True)
    description = Column(String)
    price = Column(String)

    submenu_id = Column(UUID, ForeignKey('submenus.id'))
    submenu = relationship("Submenu", back_populates="dishes")
