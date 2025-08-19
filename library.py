
import json
import os
import httpx
from typing import List, Optional
from models import Book

class Library:
    """Library class for managing book collection"""
    
    def __init__(self, data_file: str = "library.json"):
        self.data_file = data_file
        self.books: List[Book] = []
        self.load_books()
    
    def add_book(self, book: Book) -> bool:
        """Add a book to the library"""
        # Check if book with same ISBN already exists
        if self.find_book(book.isbn):
            return False
        
        self.books.append(book)
        self.save_books()
        return True
    
    def add_book_by_isbn(self, isbn: str) -> Optional[Book]:
        """Add a book to library by fetching data from Open Library API"""
        try:
            # Remove any spaces or hyphens from ISBN
            clean_isbn = isbn.replace("-", "").replace(" ", "")
            
            # Check if book already exists
            existing_book = self.find_book(clean_isbn)
            if existing_book:
                return None
            
            # Fetch book data from Open Library API
            url = f"https://openlibrary.org/isbn/{clean_isbn}.json"
            
            with httpx.Client() as client:
                response = client.get(url, timeout=10.0)
                
                if response.status_code == 404:
                    return None
                
                response.raise_for_status()
                data = response.json()
                
                # Extract title
                title = data.get("title", "Unknown Title")
                
                # Extract authors - handle different formats
                authors = []
                if "authors" in data:
                    for author_ref in data["authors"]:
                        if isinstance(author_ref, dict) and "key" in author_ref:
                            # Need to fetch author details
                            author_url = f"https://openlibrary.org{author_ref['key']}.json"
                            author_response = client.get(author_url, timeout=10.0)
                            if author_response.status_code == 200:
                                author_data = author_response.json()
                                authors.append(author_data.get("name", "Unknown Author"))
                        elif isinstance(author_ref, str):
                            authors.append(author_ref)
                
                author = ", ".join(authors) if authors else "Unknown Author"
                
                # Create and add book
                book = Book(title, author, clean_isbn)
                if self.add_book(book):
                    return book
                
        except httpx.TimeoutException:
            return None
        except httpx.RequestError:
            return None
        except json.JSONDecodeError:
            return None
        except Exception:
            return None
        
        return None
    
    def remove_book(self, isbn: str) -> bool:
        """Remove a book from the library by ISBN"""
        clean_isbn = isbn.replace("-", "").replace(" ", "")
        for i, book in enumerate(self.books): # SAfety remove using enumerate to get index
            if book.isbn == clean_isbn:
                del self.books[i]
                self.save_books()
                return True
        return False
    
    def list_books(self) -> List[Book]:
        """Return list of all books in the library"""
        return self.books.copy()
    
    def find_book(self, isbn: str) -> Optional[Book]:
        """Find a book by ISBN"""
        clean_isbn = isbn.replace("-", "").replace(" ", "")
        for book in self.books:
            if book.isbn == clean_isbn:
                return book
        return None
    
    def update_book(self, isbn: str, title: Optional[str] = None, author: Optional[str] = None) -> bool:
        """Update book information"""
        book = self.find_book(isbn)
        if not book:
            return False
        
        if title:
            book.title = title
        if author:
            book.author = author
        
        self.save_books()
        return True
    
    def load_books(self):
        """Load books from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.books = [Book.from_dict(book_data) for book_data in data]
            except (json.JSONDecodeError, KeyError, FileNotFoundError):
                self.books = []
        else:
            self.books = []
    
    def save_books(self):
        """Save books to JSON file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([book.to_dict() for book in self.books], f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving books: {e}")
    
    def search_books(self, query: str) -> List[Book]:
        """Search books by title or author"""
        query_lower = query.lower()
        results = []
        for book in self.books:
            if (query_lower in book.title.lower() or 
                query_lower in book.author.lower() or 
                query_lower in book.isbn):
                results.append(book)
        return results
    
    def get_stats(self) -> dict:
        """Get library statistics"""
        total_books = len(self.books)
        authors = set(book.author for book in self.books)
        return {
            "total_books": total_books,
            "unique_authors": len(authors),
            "authors": list(authors)
        }
    async def fetch_book_from_api(self, isbn: str) -> Book:
        """Fetch book information from Open Library API with fallback to search."""
        # normalize ISBN (remove hyphens/spaces)
        isbn_clean = isbn.replace('-', '').replace(' ', '')
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Primary: ISBN endpoint
                resp = await client.get(f"https://openlibrary.org/isbn/{isbn_clean}.json") # get directly by ISBN
                if resp.status_code == 200: #200 OK
                    data = resp.json()
                else:
                    # Fallback: search by ISBN
                    search = await client.get(f"https://openlibrary.org/search.json?isbn={isbn_clean}")
                    if search.status_code == 200:
                        sdata = search.json()
                        docs = sdata.get("docs", [])
                        if docs:
                            # take first hit and map fields
                            doc = docs[0] # take first search result
                            data = {
                                "title": doc.get("title") or doc.get("title_suggest"),
                                # authors may be an array of names on search results
                                "authors": [{"name": a} for a in (doc.get("author_name") or [])]
                            }
                        else:
                            return None
                    else:
                        return None

                # title
                title = data.get("title", "Unknown Title")

                # return authors in different formats
                authors = []
                if "authors" in data and isinstance(data["authors"], list):
                    for author_ref in data["authors"]:
                        if isinstance(author_ref, dict) and "key" in author_ref:
                            # Some results only have a reference key → need another request
                            author_key = author_ref["key"]
                            author_resp = await client.get(f"https://openlibrary.org{author_key}.json")
                            if author_resp.status_code == 200:
                                author_data = author_resp.json()
                                authors.append(author_data.get("name", "Unknown Author"))
                        elif isinstance(author_ref, str): # If no authors were found, check author_name
                            authors.append(author_ref)
                        elif isinstance(author_ref, dict) and "name" in author_ref:
                            authors.append(author_ref["name"])
                # also handle search result style
                if not authors and "author_name" in data:
                    if isinstance(data["author_name"], list):
                        authors = data["author_name"]

                # Joins authors into a single string
                author = ", ".join(authors) if authors else "Unknown Author"
                return Book(title=title, author=author, isbn=isbn_clean)

        except httpx.RequestError as e:
            print(f"Error fetching book data: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None