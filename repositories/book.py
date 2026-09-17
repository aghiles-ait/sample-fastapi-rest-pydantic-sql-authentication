from models import Book
from typing import Optional
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


def get_book_by_id(db: Session, book_id: int) -> Optional[Book]:
    return db.get(Book, book_id)

def get_books(db: Session, category: Optional[str], rating: Optional[int], year: Optional[int]) -> list[Book]:
    statement = select(Book)
    if category is not None:
        statement = statement.where(Book.category == category)
    if rating is not None:
        statement = statement.where(Book.rating == rating)
    if year is not None:
        statement = statement.where(Book.published_year == year)
    return list(db.scalars(statement).all())

def create_book(db: Session, title: str, author: str, category: str,
                rating: int, published_year: int) -> Book:
    book = Book(title=title, author=author, category=category,
                rating=rating, published_year=published_year)
    try:
        db.add(book)
        db.commit()
    except SQLAlchemyError:
        db.rollback()   # annule explicitement la transaction ratée
        raise           # cette erreur va etre catchée par FastAPI et retournera une erreur 500
    db.refresh(book)    # exécuté en cas de succès
    return book


def update_book(db: Session, book: Book, **book_updates) -> Book:
    for key, value in book_updates.items():
        setattr(book, key, value)
    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise
    db.refresh(book)
    return book

def delete_book(db: Session, book: Book) -> None:
    try:
        db.delete(book)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise
