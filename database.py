from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

SQLALCHEMY_DATABASE_URL = 'sqlite:///./base.db' # you can connect to it using "sqlite3 base.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args = {'check_same_thread': False})

SessionLocal = sessionmaker(autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
