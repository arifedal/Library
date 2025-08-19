"""
Console-based Library Management System
This is the original terminal interface for the library system.
"""

import asyncio
from api import Library, Book


class LibraryConsole:
    def __init__(self):
        self.library = Library()
    
    def display_menu(self):
        """Display the main menu"""
        print("\n" + "="*50)
        print("📚 LIBRARY MANAGEMENT SYSTEM")
        print("="*50)
        print("1. Add Book by ISBN")
        print("2. Add Book Manually") 
        print("3. List All Books")
        print("4. Search Book by ISBN")
        print("5. Delete Book")
        print("6. Show Statistics")
        print("0. Exit")
        print("-"*50)
    
    async def add_book_by_isbn(self):
        """Add a book by fetching data from Open Library API"""
        print("\n📖 Add Book by ISBN")
        isbn = input("Enter ISBN: ").strip()
        
        if not isbn:
            print("❌ ISBN cannot be empty!")
            return
        
        # Check if book already exists
        if self.library.find_book(isbn):
            print("❌ Book with this ISBN already exists!")
            return
        
        print("🔍 Fetching book information...")
        book = await self.library.fetch_book_from_api(isbn)
        
        if book:
            if self.library.add_book(book):
                print(f"✅ Successfully added: {book}")
            else:
                print("❌ Failed to add book!")
        else:
            print("❌ Book not found with the provided ISBN!")
    
    def add_book_manually(self):
        """Add a book manually with user input"""
        print("\n📝 Add Book Manually")
        title = input("Enter book title: ").strip()
        author = input("Enter author name: ").strip()
        isbn = input("Enter ISBN: ").strip()
        
        if not all([title, author, isbn]):
            print("❌ All fields are required!")
            return
        
        # Check if book already exists
        if self.library.find_book(isbn):
            print("❌ Book with this ISBN already exists!")
            return
        
        book = Book(title, author, isbn)
        if self.library.add_book(book):
            print(f"✅ Successfully added: {book}")
        else:
            print("❌ Failed to add book!")
    
    def list_books(self):
        """List all books in the library"""
        books = self.library.list_books()
        
        print(f"\n📚 Library Contents ({len(books)} books)")
        print("-"*80)
        
        if not books:
            print("📭 No books in the library yet!")
            return
        
        for i, book in enumerate(books, 1):
            print(f"{i:2d}. {book}")
    
    def search_book(self):
        """Search for a book by ISBN"""
        print("\n🔍 Search Book")
        isbn = input("Enter ISBN to search: ").strip()
        
        if not isbn:
            print("❌ ISBN cannot be empty!")
            return
        
        book = self.library.find_book(isbn)
        if book:
            print(f"📖 Found: {book}")
        else:
            print("❌ Book not found!")
    
    def delete_book(self):
        """Delete a book by ISBN"""
        print("\n🗑️  Delete Book")
        isbn = input("Enter ISBN of book to delete: ").strip()
        
        if not isbn:
            print("❌ ISBN cannot be empty!")
            return
        
        book = self.library.find_book(isbn)
        if not book:
            print("❌ Book not found!")
            return
        
        print(f"📖 Book to delete: {book}")
        confirm = input("Are you sure you want to delete this book? (y/N): ").strip().lower()
        
        if confirm == 'y':
            if self.library.remove_book(isbn):
                print("✅ Book deleted successfully!")
            else:
                print("❌ Failed to delete book!")
        else:
            print("❌ Deletion cancelled!")
    
    def show_statistics(self):
        """Show library statistics"""
        books = self.library.list_books()
        
        print("\n📊 Library Statistics")
        print("-"*30)
        print(f"Total Books: {len(books)}")
        
        if books:
            # Count unique authors
            authors = set(book.author for book in books)
            print(f"Unique Authors: {len(authors)}")
            
            # Show top authors
            author_count = {}
            for book in books:
                author_count[book.author] = author_count.get(book.author, 0) + 1
            
            if author_count:
                print("\n📝 Authors with most books:")
                sorted_authors = sorted(author_count.items(), key=lambda x: x[1], reverse=True)
                for i, (author, count) in enumerate(sorted_authors[:5], 1):
                    print(f"  {i}. {author}: {count} book{'s' if count > 1 else ''}")
    
    async def run(self):
        """Main application loop"""
        print("Welcome to the Library Management System!")
        
        while True:
            try:
                self.display_menu()
                choice = input("Enter your choice (0-6): ").strip()
                
                if choice == '0':
                    print("\n👋 Thank you for using Library Management System!")
                    break
                elif choice == '1':
                    await self.add_book_by_isbn()
                elif choice == '2':
                    self.add_book_manually()
                elif choice == '3':
                    self.list_books()
                elif choice == '4':
                    self.search_book()
                elif choice == '5':
                    self.delete_book()
                elif choice == '6':
                    self.show_statistics()
                else:
                    print("❌ Invalid choice! Please enter a number between 0-6.")
                
                # Pause before showing menu again
                if choice != '0':
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                input("Press Enter to continue...")


async def main():
    """Main entry point"""
    console = LibraryConsole()
    await console.run()


if __name__ == "__main__":
    asyncio.run(main())