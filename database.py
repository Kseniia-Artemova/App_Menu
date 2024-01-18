from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_URL

# создаем описание соединения с БД
engine = create_engine(DB_URL, echo=True)

# Создание базового класса для всех моделей. Позволяет SQLAlchemy автоматически связывать классы
# с соответствующими таблицами.
Base = declarative_base()

# Создание фабрики сессий для операций с базой данных, указанной в engine
SessionLocal = sessionmaker(bind=engine)
