from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


engine = create_engine("sqlite:///./app.db", echo=True)

session_local = sessionmaker(bind=engine)

def get_db():
    """Возвращает сессию для работы с БД"""
    db = session_local()
    try:
        yield db
    finally:
        db.close()
