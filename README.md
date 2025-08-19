# 📚 Library Management System

A library management system built with Python, featuring Object-Oriented Programming principles, external API integration, and a modern web interface powered by FastAPI.

## 🎯 Project Overview

This project demonstrates a complete progression from a simple console application to a full-featured web service:

- **Stage 1**: Object-Oriented Programming (OOP) with console interface
- **Stage 2**: External API integration with Open Library Books API
- **Stage 3**: RESTful web API using FastAPI with interactive documentation
- **Advanced Features**: Modern web interface, comprehensive testing, and enhanced functionality

## ✨ Features

### Core Functionality
- ✅ Add books manually or by ISBN (auto-fetch from Open Library API)
- ✅ Remove books by ISBN
- ✅ List all books in the library
- ✅ Search books by title, author, or ISBN
- ✅ Update book information
- ✅ Persistent data storage in JSON format
- ✅ Library statistics and analytics

### Advanced Features
- 🌐 Modern responsive web interface
- 🔍 Real-time search functionality
- 📊 Library statistics dashboard
- 🎨 Beautiful UI with gradient backgrounds and animations
- 📱 Mobile-responsive design
- 🧪 Comprehensive test coverage
- 📖 Interactive API documentation

## 🛠 Technology Stack

- **Backend**: Python 3.8+, FastAPI, Uvicorn
- **HTTP Client**: httpx for API requests
- **Testing**: pytest, pytest-asyncio
- **Data Storage**: JSON files
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **API Documentation**: OpenAPI/Swagger (auto-generated)

## 📁 Project Structure

```
library-management-system/
├── models.py              # Book class and Pydantic models
├── library.py             # Library class with core functionality
├── main.py               # Console application (Stages 1 & 2)
├── api.py                # FastAPI application (Stage 3)
├── test_library.py       # Comprehensive test suite
├── requirements.txt      # Python dependencies
├── library.json          # Data storage (auto-generated)
├── static/               # Web interface files
│   └── index.html        # Modern web interface
└── README.md            # Project documentation
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/library-management-system.git
cd library-management-system
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

## 📖 Usage

### Console Application (Stages 1 & 2)

Run the terminal-based application:

```bash
python main.py
```

**Available Menu Options:**
1. Add Book (by ISBN) - Fetches data from Open Library API
2. Add Book (manually) - Enter all book details manually
3. Remove Book - Remove by ISBN
4. List All Books - Display all books in library
5. Search Books - Search by title, author, or ISBN
6. Find Book by ISBN - Find specific book
7. Update Book - Modify book information
8. Library Statistics - View collection stats
9. Exit

### Web API Server (Stage 3)

Start the FastAPI server:

```bash
uvicorn api:app --reload
```

The server will start at `http://localhost:8000`

**Available Interfaces:**
- 🏠 **Web Interface**: http://localhost:8000
- 📚 **API Documentation**: http://localhost:8000/docs
- 🔧 **Alternative API Docs**: http://localhost:8000/redoc

### Production Deployment

For production deployment:

```bash
py -3 -m uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🔌 API Endpoints

### Books Management

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| `GET` | `/books` | Get all books | None |
| `GET` | `/books/{isbn}` | Get book by ISBN | None |
| `POST` | `/books` | Add book by ISBN | `{"isbn": "978-0-123456-78-9"}` |
| `POST` | `/books/manual` | Add book manually | `{"title": "Book Title", "author": "Author Name", "isbn": "978-0-123456-78-9"}` |
| `PUT` | `/books/{isbn}` | Update book | `{"title": "New Title", "author": "New Author", "isbn": "978-0-123456-78-9"}` |
| `DELETE` | `/books/{isbn}` | Delete book | None |

### Utility Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/` | Serve web interface |

### Example API Requests

**Add Book by ISBN:**
```bash
curl -X POST "http://localhost:8000/books" \
     -H "Content-Type: application/json" \
     -d '{"isbn": "978-0-7432-7356-5"}'
```

**Add Book Manually:**
```bash
curl -X POST "http://localhost:8000/books/manual" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "The Great Gatsby",
       "author": "F. Scott Fitzgerald",
       "isbn": "978-0-7432-7356-5"
     }'
```

**Get All Books:**
```bash
curl -X GET "http://localhost:8000/books"
```

**Delete Book:**
```bash
curl -X DELETE "http://localhost:8000/books/978-0-7432-7356-5"
```

## 🧪 Testing

The project includes comprehensive test coverage for all functionality.

### Run All Tests
```bash
pytest test_library.py -v
```

### Run Specific Test Categories
```bash
# Test Book class
pytest test_library.py::TestBook -v

# Test Library class
pytest test_library.py::TestLibrary -v

# Test FastAPI endpoints
pytest test_library.py::TestFastAPIEndpoints -v
```

### Test Coverage Areas

- ✅ **Book Class**: Creation, serialization, deserialization
- ✅ **Library Operations**: Add, remove, find, list, search books
- ✅ **Data Persistence**: JSON save/load functionality
- ✅ **API Integration**: Open Library API calls with mocking
- ✅ **FastAPI Endpoints**: All CRUD operations
- ✅ **Error Handling**: Invalid inputs, API failures, edge cases

### Sample Test Output
```
test_library.py::TestBook::test_book_creation PASSED
test_library.py::TestLibrary::test_add_book PASSED
test_library.py::TestFastAPIEndpoints::test_add_book_by_isbn_success PASSED
```

## 🔧 Dependencies

### Production Dependencies (`requirements.txt`)
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
httpx==0.25.2
pydantic==2.5.0
```

### Development Dependencies
```
pytest==7.4.3
pytest-asyncio==0.21.1
```

## 📊 Data Format

Books are stored in `library.json` with the following structure:

```json
[
  {
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "isbn": "978-0-7432-7356-5"
  },
  {
    "title": "1984",
    "author": "George Orwell",
    "isbn": "978-0-452-28423-4"
  }
]
```

## 🌟 Advanced Features

### Web Interface Highlights
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Updates**: Live statistics and instant feedback
- **Modern UI**: Gradient backgrounds, animations, and hover effects
- **Search Functionality**: Live search as you type
- **CRUD Operations**: Full create, read, update, delete functionality

### Error Handling
- Graceful handling of API failures
- User-friendly error messages
- Input validation and sanitization
- Network timeout handling

### Performance Features
- Efficient JSON serialization
- Async API calls for better performance
- Client-side caching for better UX

## 🔍 Open Library API Integration

This project integrates with the [Open Library Books API](https://openlibrary.org/developers/api) to automatically fetch book information:

- **Endpoint**: `https://openlibrary.org/isbn/{isbn}.json`
- **Features**: Automatic title and author extraction
- **Error Handling**: Graceful fallback for invalid ISBNs
- **Rate Limiting**: Respectful API usage

## 🚦 Project Development Stages

### Stage 1: OOP Console Application ✅
- Book and Library classes
- Basic CRUD operations
- JSON persistence
- Menu-driven interface

### Stage 2: API Integration ✅
- Open Library API integration
- HTTP client implementation
- Error handling and validation
- Enhanced console interface

### Stage 3: FastAPI Web Service ✅
- RESTful API endpoints
- Pydantic data models
- Interactive documentation
- CORS support for web interface

### Advanced Enhancements ✅
- Modern web interface
- Comprehensive testing
- Enhanced error handling
- Performance optimizations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@arifedal]((https://github.com/arifedal)
- LinkedIn: (https://www.linkedin.com/in/arifedal/)

## 🙏 Acknowledgments

- [Open Library](https://openlibrary.org/) for providing the free books API
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [Global AI Hub](https://globalaihub.com/) for the Python 202 Bootcamp


---

**Made with ❤️ for Global AI Hub Python 202 Bootcamp**
