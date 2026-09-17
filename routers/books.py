from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Path, Query

from sqlalchemy.orm import Session
from database import get_db

from repositories import book as book_repository
from schemas.book import BookResponse, BookPostPutRequest, BookPatchRequest

router = APIRouter(prefix="/books", tags=["books"])

@router.get("", response_model=list[BookResponse], status_code=200)
def get_books(db: Annotated[Session, Depends(get_db)],
              category: Optional[str] = None,
              rating: Annotated[Optional[int], Query(ge=0, le=5)] = None,
              year: Annotated[Optional[int], Query(ge=1000, le=2026)] = None):
    return book_repository.get_books(db, category, rating, year)

@router.get("/{book_id}", response_model=BookResponse) # select resource using path param
def get_book(book_id: Annotated[int, Path(gt=0)], db: Annotated[Session, Depends(get_db)]):
    book = book_repository.get_book_by_id(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("", status_code=201, response_model=BookResponse) # create resource using body
def create_book(book_request: BookPostPutRequest, db: Annotated[Session, Depends(get_db)]):
    return book_repository.create_book(db, **book_request.model_dump())

@router.put("/{book_id}", status_code=204) # update resource using body
def update_book(book_id: Annotated[int, Path(gt=0)], book_updates: BookPostPutRequest, db: Annotated[Session, Depends(get_db)]):
    book = book_repository.get_book_by_id(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    book_repository.update_book(db, book, **book_updates.model_dump())

@router.patch("/{book_id}", status_code=204) # partial resource update using body
def partial_update_book(book_id: Annotated[int, Path(gt=0)], book_updates: BookPatchRequest, db: Annotated[Session, Depends(get_db)]):
    book = book_repository.get_book_by_id(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    else:
        book_repository.update_book(db, book, **book_updates.model_dump(exclude_unset=True)) # exclude unset properties

@router.delete("/{book_id}", status_code=204) # delete resource using path param
def delete_book(book_id: Annotated[int, Path(gt=0)], db: Annotated[Session, Depends(get_db)]):
    book = book_repository.get_book_by_id(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    book_repository.delete_book(db, book)
