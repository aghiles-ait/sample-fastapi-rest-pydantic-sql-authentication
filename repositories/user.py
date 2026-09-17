from models import User
from typing import Optional
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.get(User, user_id)

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.scalars(select(User).where(User.username == username)).first()

def create_user(db: Session, username: str, hashed_password: str) -> User:
    user = User(username=username, hashed_password=hashed_password)
    try:
        db.add(user)
        db.commit()
    except SQLAlchemyError:
        db.rollback()   # annule explicitement la transaction ratée
        raise           # laissée remonter : c'est à la route de la traduire en code HTTP
    db.refresh(user)    # exécuté en cas de succès
    return user
