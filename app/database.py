from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from config import DB_URL

# создаем описание соединения с БД
engine = create_async_engine(DB_URL, echo=True)

# Создание базового класса для всех моделей. Позволяет SQLAlchemy автоматически связывать классы
# с соответствующими таблицами.
Base = declarative_base()

# Создание фабрики сессий для операций с базой данных, указанной в engine
async_session_maker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Генератор для запуска асинхронной сессии"""
    async with async_session_maker() as session:
        yield session