"""
Comprehensive tests for the Library Management System
"""

import pytest
import os
import json
import tempfile
from unittest.mock import patch, AsyncMock
import httpx
from fastapi.testclient import TestClient

# Import your modules
from api import app, Book, Library


class TestBook:
    """Test the Book class"""
    
    def test_book_creation(self):
        """Test book object creation"""
        book = Book("1984", "George Orwell", "978-0-452-28423-4")
        assert book.title == "1984"
        assert book.author == "George Orwell"
        assert book.isbn == "978-0-452-28423-4"
    
    def test_book_to_dict(self):
        """Test book to dictionary conversion"""
        book = Book("1984", "George Orwell", "978-0-452-28423-4")
        book_dict = book.to_dict()
        expected = {
            "title": "1984",
            "author": "George Orwell",
            "isbn": "978-0-452-28423-4"
        }
        assert book_dict == expected
    
    def test_book_from_dict(self):
        """Test book creation from dictionary"""
        book_data = {
            "title": "1984",
            "author": "George Orwell",
            "isbn": "978-0-452-28423-4"
        }
        book = Book.from_dict(book_data)
        assert book.title == "1984"
        assert book.author == "George Orwell"
        assert book.isbn == "978-0-452-28423-4"


class TestLibrary:
    """Test the Library class"""
    
    @pytest.fixture #simulation
    def temp_library(self):
        """Create a temporary library for testing"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
            temp_filename = temp_file.name
        
        library = Library(temp_filename)
        yield library
        
        # Cleanup
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
    
    #library starts empty.
    def test_library_initialization(self, temp_library):
        """Test library initialization"""
        assert isinstance(temp_library.books, list)
        assert len(temp_library.books) == 0
    
    # adding a book works
    def test_add_book(self, temp_library):
        """Test adding a book to the library"""
        book = Book("1984", "George Orwell", "978-0-452-28423-4")
        result = temp_library.add_book(book)
        
        assert result is True
        assert len(temp_library.books) == 1
        assert temp_library.books[0].title == "1984"
    
    # cannot add a book with the same ISBN
    def test_add_duplicate_book(self, temp_library):
        """Test adding a book with duplicate ISBN"""
        book1 = Book("1984", "George Orwell", "978-0-452-28423-4")
        book2 = Book("Different Title", "Different Author", "978-0-452-28423-4")
        
        temp_library.add_book(book1)
        result = temp_library.add_book(book2)
        
        assert result is False
        assert len(temp_library.books) == 1
    
    # deleting a book works.
    def test_remove_book(self, temp_library):
        """Test removing a book from the library"""
        book = Book("1984", "George Orwell", "978-0-452-28423-4")
        temp_library.add_book(book)
        
        result = temp_library.remove_book("978-0-452-28423-4")
        assert result is True
        assert len(temp_library.books) == 0
    
    # deleting a book that isn’t there returns "False"
    def test_remove_nonexistent_book(self, temp_library):
        """Test removing a book that doesn't exist"""
        result = temp_library.remove_book("nonexistent-isbn")
        assert result is False
    
    # can find an existing book, returns None if not found.
    def test_find_book(self, temp_library):
        """Test finding a book by ISBN"""
        book = Book("1984", "George Orwell", "978-0-452-28423-4")
        temp_library.add_book(book)
        
        found_book = temp_library.find_book("978-0-452-28423-4")
        assert found_book is not None
        assert found_book.title == "1984"
        
        not_found = temp_library.find_book("nonexistent-isbn")
        assert not_found is None
    
    # listing books returns a list of books.
    def test_list_books(self, temp_library):
        """Test listing all books"""
        book1 = Book("1984", "George Orwell", "978-0-452-28423-4")
        book2 = Book("Animal Farm", "George Orwell", "978-0-452-28424-1")
        
        temp_library.add_book(book1)
        temp_library.add_book(book2)
        
        books = temp_library.list_books()
        assert len(books) == 2
        assert isinstance(books, list)
    
    # checks that saving to JSON and loading back works.
    def test_save_and_load_books(self, temp_library):
        """Test saving and loading books from file"""
        book = Book("1984", "George Orwell", "978-0-452-28423-4")
        temp_library.add_book(book)
        
        # Create new library instance with same file
        new_library = Library(temp_library.filename)
        
        assert len(new_library.books) == 1
        assert new_library.books[0].title == "1984"
    
    # can fetch book details from an external API
    @pytest.mark.asyncio
    async def test_fetch_book_from_api_success(self, temp_library):
        """Test successful API fetch"""
        mock_response_data = {
            "title": "The Great Gatsby",
            "authors": [{"key": "/authors/OL23919A"}]
        }
        
        mock_author_data = {
            "name": "F. Scott Fitzgerald"
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_client_instance
            
            # Mock the book data response
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_response_data
            
            # Mock the author data response
            mock_author_response = AsyncMock()
            mock_author_response.status_code = 200
            mock_author_response.json.return_value = mock_author_data
            
            mock_client_instance.get.side_effect = [mock_response, mock_author_response]
            
            book = await temp_library.fetch_book_from_api("978-0-7432-7356-5")
            
            assert book is not None
            assert book.title == "The Great Gatsby"
            assert book.author == "F. Scott Fitzgerald"
            assert book.isbn == "978-0-7432-7356-5"
    
    @pytest.mark.asyncio
    async def test_fetch_book_from_api_not_found(self, temp_library):
        """Test API fetch when book is not found"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_client_instance
            
            mock_response = AsyncMock()
            mock_response.status_code = 404
            
            mock_client_instance.get.return_value = mock_response
            
            book = await temp_library.fetch_book_from_api("invalid-isbn")
            
            assert book is None


class TestFastAPIEndpoints:
    """Test FastAPI endpoints"""
    
    @pytest.fixture #simulation
    def client(self):
        """Create a test client"""
        return TestClient(app)
    
    def test_read_index(self, client):
        """Test serving the index page"""
        response = client.get("/")
        assert response.status_code in [200, 404]  # 404 if file doesn't exist
    
    def test_health_check(self, client): # returns status
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "total_books" in data
        assert "version" in data
    
    def test_get_all_books_empty(self, client):
        """Test getting all books when library is empty"""
        response = client.get("/books")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_add_book_manual(self, client):
        """Test adding a book manually"""
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "isbn": "978-1-234-56789-0"
        }
        
        response = client.post("/books/manual", json=book_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Book"
        assert data["author"] == "Test Author"
        assert data["isbn"] == "978-1-234-56789-0"
    
    def test_add_duplicate_book_manual(self, client):
        """Test adding a duplicate book manually"""
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "isbn": "978-1-234-56789-1"
        }
        
        # Add book first time
        response1 = client.post("/books/manual", json=book_data)
        assert response1.status_code == 201
        
        # Try to add same book again
        response2 = client.post("/books/manual", json=book_data)
        assert response2.status_code == 400
        assert "already exists" in response2.json()["detail"]
    
    def test_get_book_by_isbn(self, client):
        """Test getting a book by ISBN"""
        # First add a book
        book_data = {
            "title": "Test Book",
            "author": "Test Author", 
            "isbn": "978-1-234-56789-2"
        }
        client.post("/books/manual", json=book_data)
        
        # Then get it
        response = client.get("/books/978-1-234-56789-2")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Book"
    
    def test_get_nonexistent_book(self, client):
        """Test getting a book that doesn't exist"""
        response = client.get("/books/nonexistent-isbn")
        assert response.status_code == 404
    
    def test_delete_book(self, client):
        """Test deleting a book"""
        # First add a book
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "isbn": "978-1-234-56789-3"
        }
        client.post("/books/manual", json=book_data)
        
        # Then delete it
        response = client.delete("/books/978-1-234-56789-3")
        assert response.status_code == 200
        
        # Verify it's gone
        get_response = client.get("/books/978-1-234-56789-3")
        assert get_response.status_code == 404
    
    def test_delete_nonexistent_book(self, client):
        """Test deleting a book that doesn't exist"""
        response = client.delete("/books/nonexistent-isbn")
        assert response.status_code == 404
    
    @patch('api.Library.fetch_book_from_api')
    def test_add_book_by_isbn_success(self, mock_fetch, client):
        """Test adding a book by ISBN with mocked API call"""
        # Mock the API call
        mock_book = Book("Mocked Book", "Mocked Author", "978-1-234-56789-4")
        mock_fetch.return_value = mock_book
        
        response = client.post("/books", json={"isbn": "978-1-234-56789-4"})
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Mocked Book"
    
    @patch('api.Library.fetch_book_from_api')
    def test_add_book_by_isbn_not_found(self, mock_fetch, client):
        """Test adding a book by ISBN when API returns None"""
        mock_fetch.return_value = None
        
        response = client.post("/books", json={"isbn": "invalid-isbn"})
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])