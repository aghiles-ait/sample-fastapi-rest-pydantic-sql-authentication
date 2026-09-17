from database import Base
from datetime import date, datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[str] = mapped_column(default='user')

class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    author: Mapped[str] = mapped_column()
    category: Mapped[str] = mapped_column()
    rating: Mapped[int] = mapped_column()
    published_year: Mapped[int] = mapped_column()

class Loan(Base):
    __tablename__ = 'loans'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'))
    borrowed_at: Mapped[datetime] = mapped_column(default=datetime.now)
    due_date: Mapped[date] = mapped_column()
    returned_at: Mapped[datetime | None] = mapped_column(default=None)

