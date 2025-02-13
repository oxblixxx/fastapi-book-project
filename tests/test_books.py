import pytest
from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app
from api.db.schemas import Book, Genre, InMemoryDB

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    # Reset the in-memory database before each test
    db = InMemoryDB()
    db.books = {
        1: Book(
            id=1,
            title="The Hobbit",
            author="J.R.R. Tolkien",
            publication_year=1937,
            genre=Genre.FANTASY,
        ),
        2: Book(
            id=2,
            title="The Lord of the Rings",
            author="J.R.R. Tolkien",
            publication_year=1954,
            genre=Genre.FANTASY,
        ),
        3: Book(
            id=3,
            title="The Return of the King",
            author="J.R.R. Tolkien",
            publication_year=1955,
            genre=Genre.FANTASY,
        ),
    }

def test_get_all_books(client):
    response = client.get("/books/")
    assert response.status_code == 200
    assert len(response.json()) == 3

def test_get_single_book(client):
    response = client.get("/books/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "The Hobbit"
    assert data["author"] == "J.R.R. Tolkien"

def test_get_nonexistent_book(client):
    response = client.get("/books/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}

def test_create_book(client):
    new_book = {
        "id": 4,
        "title": "Harry Potter and the Sorcerer's Stone",
        "author": "J.K. Rowling",
        "publication_year": 1997,
        "genre": "Fantasy",
    }
    response = client.post("/books/", json=new_book)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 4
    assert data["title"] == "Harry Potter and the Sorcerer's Stone"

def test_create_book_invalid_data(client):
    invalid_book = {
        "id": 5,
        "title": "",  # Missing title
        "author": "J.K. Rowling",
        "publication_year": 1997,
        "genre": "Fantasy",
    }
    response = client.post("/books/", json=invalid_book)
    assert response.status_code == 422  # Unprocessable Entity

def test_update_book(client):
    updated_book = {
        "id": 1,
        "title": "The Hobbit: An Unexpected Journey",
        "author": "J.R.R. Tolkien",
        "publication_year": 1937,
        "genre": "Fantasy",
    }
    response = client.put("/books/1", json=updated_book)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "The Hobbit: An Unexpected Journey"

def test_update_nonexistent_book(client):
    updated_book = {
        "id": 999,
        "title": "Nonexistent Book",
        "author": "Unknown",
        "publication_year": 2023,
        "genre": "Mystery",
    }
    response = client.put("/books/999", json=updated_book)
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}

def test_delete_book(client):
    response = client.delete("/books/3")
    assert response.status_code == 204

    response = client.get("/books/3")
    assert response.status_code == 404

def test_delete_nonexistent_book(client):
    response = client.delete("/books/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}
