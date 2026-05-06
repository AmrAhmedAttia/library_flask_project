class Book:
    def __init__(self, book_id, title, author, copies):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.copies = copies
        self.available = copies

    def to_dict(self):
        return {
            "id": self.book_id,
            "title": self.title,
            "author": self.author,
            "copies": self.copies,
            "available": self.available
        }


class PhysicalBook(Book):
    def to_dict(self):
        book_data = super().to_dict()
        book_data["type"] = "Physical"
        return book_data


class EBook(Book):
    def to_dict(self):
        book_data = super().to_dict()
        book_data["type"] = "E-Book"
        return book_data


class BookFactory:
    @staticmethod
    def create_book(book_id, title, author, book_type, copies):
        if book_type == "Physical":
            return PhysicalBook(book_id, title, author, copies)

        elif book_type == "E-Book":
            return EBook(book_id, title, author, copies)

        else:
            raise ValueError("Invalid book type")