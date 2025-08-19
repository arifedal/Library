from pydantic import BaseModel
from typing import Optional
import json

class Book:
    """Book class representing a single book in the library"""
    
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn
    
    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"
    
    def to_dict(self):
        """Convert Book object to dictionary for JSON serialization"""
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create Book object from dictionary"""
        return cls(data["title"], data["author"], data["isbn"])

# Pydantic models for FastAPI
class BookModel(BaseModel):
    title: str
    author: str
    isbn: str

class BookCreate(BaseModel):
    isbn: str

class BookResponse(BaseModel):
    title: str
    author: str
    isbn: str
    
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None