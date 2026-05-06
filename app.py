from flask import Flask, render_template, request, redirect
from book_factory import BookFactory

app = Flask(__name__)

books = [
    {
        "id": "B001",
        "title": "زقاق المدق",
        "author": "نجيب محفوظ",
        "type": "Physical",
        "copies": 2,
        "available": 2
    },
    {
        "id": "B002",
        "title": "Clean Code",
        "author": "Robert Martin",
        "type": "E-Book",
        "copies": 1,
        "available": 1
    },
    {
        "id": "B003",
        "title": "الأمير الصغير",
        "author": "Antoine de Saint",
        "type": "Physical",
        "copies": 1,
        "available": 1
    }
]

members = [
    {
        "id": "M001",
        "name": "أحمد محمد",
        "type": "Student"
    },
    {
        "id": "M002",
        "name": "سارة علي",
        "type": "Senior"
    },
    {
        "id": "M003",
        "name": "محمود حسن",
        "type": "Staff"
    }
]

borrowed_books = []


@app.route("/")
def home():
    total_copies = 0
    available_books = 0

    for book in books:
        total_copies += book["copies"]
        available_books += book["available"]

    return render_template(
        "index.html",
        books=books,
        members=members,
        borrowed_books=borrowed_books,
        total_copies=total_copies,
        available_books=available_books
    )


@app.route("/add_book", methods=["POST"])
def add_book():
    book_id = request.form["book_id"]
    title = request.form["title"]
    author = request.form["author"]
    book_type = request.form["book_type"]
    copies = int(request.form["copies"])

    book = BookFactory.create_book(
        book_id,
        title,
        author,
        book_type,
        copies
    )

    books.append(book.to_dict())

    return redirect("/")


@app.route("/add_member", methods=["POST"])
def add_member():
    member_id = request.form["member_id"]
    member_name = request.form["member_name"]
    member_type = request.form["member_type"]

    new_member = {
        "id": member_id,
        "name": member_name,
        "type": member_type
    }

    members.append(new_member)

    return redirect("/")


@app.route("/borrow_book", methods=["POST"])
def borrow_book():
    member_id = request.form["member_id"]
    book_id = request.form["book_id"]

    selected_member = None
    selected_book = None

    for member in members:
        if member["id"] == member_id:
            selected_member = member

    for book in books:
        if book["id"] == book_id:
            selected_book = book

    if selected_member and selected_book and selected_book["available"] > 0:
        selected_book["available"] -= 1

        borrowed_books.append({
            "member_id": selected_member["id"],
            "member_name": selected_member["name"],
            "book_id": selected_book["id"],
            "book_title": selected_book["title"]
        })

    return redirect("/")


@app.route("/return_book", methods=["POST"])
def return_book():
    record_index = int(request.form["record_index"])

    returned_record = borrowed_books.pop(record_index)

    for book in books:
        if book["id"] == returned_record["book_id"]:
            book["available"] += 1

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)