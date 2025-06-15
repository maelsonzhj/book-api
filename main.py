from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Используем список books для хранения данных
books = []

# Создаем класс Book, который будет описывать JSON при принятии методов
class Book(BaseModel):
    id: str
    title: str
    author: str
    
class BookCreate(BaseModel):
    title: str
    author: str


# Запуск базового сервера 
@app.get("/")
async def read_root():
    return {"message": "Hello World!"}

# Ручки
@app.get("/books")
async def get_books():
    return books

@app.get("/books/{id}")
async def find_book_id(id: str):
    for book in books:
        if book["id"] == id:
            return book
    return {"error": "Книга не найдена"}, 404

@app.post("/books")
async def create_book(book_data: BookCreate):
    new_id = str(len(books) + 1)
    new_book = BookCreate(title=book_data.title, author=book_data.author)
    books.append(new_book.dict())
    return new_book, 201

@app.put("/books/{id}")
async def replaces_book(id: str, book_data: BookCreate):
    get_request_body = BookCreate(title=book_data.title, author=book_data.author)
    for book in books:
        if book["id"] == id:
            book["title"] = book_data.title
            book["author"] = book_data.author
            return book
    return {"error": "Книга не найдена"}, 404


@app.delete("/books/{id}")
async def delete_book(id: str):
    for book in books:
        if book["id"] == id:
            books.remove(book)
            return {"message": "Книга успешно удалена"}
    return {"error": "Книга по id не найдена"}, 404
    


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
