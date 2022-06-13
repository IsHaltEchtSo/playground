from pydantic import BaseModel
from typing import List, Optional
from datetime import date
import json

class Book(BaseModel):
    title: str
    author: str
    year: int = date.today().year
    subtitle: Optional[str]

books: List[Book]

with open('data/books.json') as file:
    data = json.load(file)
    books = [Book(**book) for book in data]

print(books[1])
