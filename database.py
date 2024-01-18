from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# создаем описание соединения с БД
engine = create_engine("postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DB_HOST}/{DATABASE_NAME}",
                       echo=True
                       )

# Создание базового класса для всех моделей. Позволяет SQLAlchemy автоматически связывать классы
# с соответствующими таблицами.
Base = declarative_base()

# Создание фабрики сессий для операций с базой данных, указанной в engine
SessionLocal = sessionmaker(bind=engine)
