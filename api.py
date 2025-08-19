"""
FastAPI application for the Library Management System.
Serves both the web interface and API endpoints.
"""
import os
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import httpx
import json
import os

from library import Library
from models import Book

# Pydantic models for API
class BookCreate(BaseModel):
    isbn: str

class BookManual(BaseModel):
    title: str
    author: str
    isbn: str

class BookResponse(BaseModel):
    title: str
    author: str
    isbn: str

# Initialize app
app = FastAPI(title="Library Management System API", version="1.0.0")

# CORS (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize library
library = Library()

# Mount static files (for serving the HTML interface)
# Create static directory if it doesn't exist
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


# Root endpoint - serve the HTML interface
@app.get("/")
async def read_index():
    index_path = os.path.join("static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Index not found. Create static/index.html or visit /docs for API."}


# API Endpoints
@app.get("/books", response_model=List[BookResponse])
async def get_all_books():
    """Get all books in the library"""
    books = library.list_books()
    return [BookResponse(**book.to_dict()) for book in books]

# Path operations for from API
@app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def add_book_by_isbn(book_data: BookCreate):
    """Add a book by ISBN (fetches data from Open Library API)"""
    isbn = book_data.isbn.strip()
    
    # Check if book already exists
    existing_book = library.find_book(isbn)
    if existing_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book with this ISBN already exists"
        )
    
    # Fetch book data from API
    book = await library.fetch_book_from_api(isbn)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found with the provided ISBN"
        )
    
    # Add book to library
    if library.add_book(book):
        return BookResponse(**book.to_dict())
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to add book"
        )

# Path operations manually
@app.post("/books/manual", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def add_book_manual(book_data: BookManual):
    """Add a book manually with all details provided"""
    isbn = book_data.isbn.strip()
    
    # Check if book already exists
    existing_book = library.find_book(isbn)
    if existing_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book with this ISBN already exists"
        )
    
    # Create book object
    book = Book(
        title=book_data.title.strip(),
        author=book_data.author.strip(),
        isbn=isbn
    )
    
    # Add book to library
    if library.add_book(book):
        return BookResponse(**book.to_dict())
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to add book"
        )


@app.delete("/books/{isbn}")
async def delete_book(isbn: str):
    """Delete a book by ISBN"""
    if library.remove_book(isbn):
        return {"message": "Book deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )


@app.get("/books/{isbn}", response_model=BookResponse)
async def get_book_by_isbn(isbn: str):
    """Get a specific book by ISBN"""
    book = library.find_book(isbn)
    if book:
        return BookResponse(**book.to_dict())
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
#Update book details
@app.put("/books/{isbn}", response_model=BookResponse)
async def update_book(isbn: str, book_data: BookManual):
    """Update a book (title, author, optional isbn)."""
    isbn = isbn.strip()
    book = library.find_book(isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    new_isbn = book_data.isbn.strip()
    if new_isbn != isbn and library.find_book(new_isbn):
        raise HTTPException(status_code=409, detail="Another book with that ISBN already exists")

    book.title = book_data.title.strip()
    book.author = book_data.author.strip()
    book.isbn = new_isbn
    library.save_books()
    return BookResponse(**book.to_dict())

# Health check endpoint everything is running
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "total_books": len(library.books),
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)