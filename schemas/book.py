from pydantic import BaseModel, Field
from typing import Optional

class BookPostPutRequest(BaseModel):
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    category: str = Field(min_length=3)
    rating: int = Field(ge=0, le=5)
    published_year: int = Field(ge=1000, le=2026)

    model_config = {
        "json_schema_extra" : {
            "example": {
                "title": "A new book",
                "author": "Aghiles",
                "category": "science",
                "rating": 5,
                "published_year": 2026
            }
        }
    }

class BookPatchRequest(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3)
    author: Optional[str] = Field(default=None, min_length=1)
    category: Optional[str] = Field(default=None, min_length=3)
    rating: Optional[int] = Field(default=None, ge=0, le=5)
    published_year: Optional[int] = Field(default=None, ge=1000, le=2026)


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    category: str
    rating: int
    published_year: int

    model_config = {"from_attributes": True}   # authorize Pydantic to read an ORM object
