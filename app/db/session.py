from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Подключение к БД
engine = create_engine(settings.DATABASE_URL)

# Фабрика сессий (каждый запрос будет получать свою сессию)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для всех моделей (Entity)
Base = declarative_base()

# Вспомогательная функция для получения сессии в контроллерах
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()