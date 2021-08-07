from flask.blueprints import Blueprint
from flask import Blueprint, render_template, request, flash, redirect, url_for
from libman.models import Book
from libman.application import db
from libman.forms import AddBookForm, EditBookForm
import random, requests
from datetime import datetime

book = Blueprint("books", __name__, url_prefix="/books")


# GET - /books
@book.route("/", methods=["GET"])
def index():

    # Search.
    search = request.args.get("s")
    if search:
        books = Book.query.filter((Book.title + " " + Book.authors).like(f"%{search}%"))
        flash((f"Search results for : {search}",), category="info")
    else:
        books = Book.query.all()

    return render_template("books/index.html", books=books)


# GET & POST - /books/add
@book.route("/add", methods=["GET", "POST"])
def add():
    form = AddBookForm()

    # Add book to database.
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            authors=form.authors.data,
            average_rating=form.average_rating.data,
            isbn=form.isbn.data,
            isbn13=form.isbn13.data,
            language_code=form.language_code.data,
            num_pages=form.num_pages.data,
            ratings_count=form.ratings_count.data,
            text_reviews_count=form.text_reviews_count.data,
            publication_date=form.publication_date.data,
            publisher=form.publisher.data,
            quantity=form.quantity.data,
            rent=form.rent.data,
        )
        db.session.add(book)
        db.session.commit()
        flash(
            (f"Book added with Book ID = {book.book_id}.",),
            category="success",
        )
        return redirect(url_for("books.index"))

    # Flash error messages.
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg, category="danger")
    else:
        form.average_rating.data = round(random.uniform(1, 5), 1)
        form.isbn.data = random.randrange(1000000000, 10000000000)
        form.isbn13.data = random.randrange(1000000000000, 10000000000000)
        form.language_code.data = random.choice(
            ["eng", "spa", "en-GB", "en-US", "ger", "enm"]
        )
        form.num_pages.data = random.randint(1, 1000)
        form.ratings_count.data = random.randint(1, 1000)
        form.text_reviews_count.data = random.randint(1, 1000)
        form.quantity.data = random.randint(1, 10)
        form.rent.data = random.randint(50, 100)

    return render_template("books/add.html", form=form)


# POST - /books/remove
@book.route("/remove", methods=["POST"])
def remove():
    # Get book through book_id.
    book = Book.query.filter_by(book_id=request.form.get("book_id")).first()
    message = f"Book with Book ID = {book.book_id} "
    if book:
        db.session.delete(book)
        db.session.commit()
        message += "has been removed."
    else:
        message += "does not found or it has been removed earlier."
    flash(
        (f"{message}",),
        category="warning",
    )
    return redirect(url_for("books.index"))


# GET - /books/details<id>
@book.route("/details/<id>", methods=["GET"])
def details(id):
    book = Book.query.filter_by(book_id=id).first()
    return render_template("books/details.html", book=book, id=id)


# GET & POST - /books/edit/<id>
@book.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    form = EditBookForm()
    book = Book.query.filter_by(book_id=id).first()

    # Update and save book to database.
    if form.validate_on_submit():
        book.title = form.title.data
        book.authors = form.authors.data
        book.average_rating = form.average_rating.data
        book.isbn = form.isbn.data
        book.isbn13 = form.isbn13.data
        book.language_code = form.language_code.data
        book.num_pages = form.num_pages.data
        book.ratings_count = form.ratings_count.data
        book.text_reviews_count = form.text_reviews_count.data
        book.publication_date = form.publication_date.data
        book.publisher = form.publisher.data
        book.quantity = form.quantity.data
        book.rent = form.rent.data
        db.session.commit()

        flash(
            (f"Book updated with Book ID = {form.book_id.data}.",),
            category="success",
        )
        return redirect(url_for("books.index"))

    # Flash error messages.
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg, category="danger")
    else:
        # Set value for form attributes using book instance.
        if book:
            form.book_id.data = book.book_id
            form.title.data = book.title
            form.authors.data = book.authors
            form.average_rating.data = book.average_rating
            form.isbn.data = book.isbn
            form.isbn13.data = book.isbn13
            form.language_code.data = book.language_code
            form.num_pages.data = book.num_pages
            form.ratings_count.data = book.ratings_count
            form.text_reviews_count.data = book.text_reviews_count
            form.publication_date.data = book.publication_date
            form.publisher.data = book.publisher
            form.quantity.data = book.quantity
            form.rent.data = book.rent

    return render_template("books/edit.html", form=form, id=id)


# POST - /books/seed
@book.route("/seed", methods=["POST"])
def seed():
    response = requests.get("https://frappe.io/api/method/frappe-library")
    json_response = response.json()
    books = list(json_response["message"])

    # Get existing book id's in a list.
    existing_book_ids = []
    for book_id in db.session.query(Book.book_id).all():
        existing_book_ids.append(book_id[0])

    skipped_book_count = 0
    for book in books:
        # Only add those books, which are not available in the database.
        if int(book["bookID"]) not in existing_book_ids:
            new_book = Book(
                title=book["title"],
                authors=book["authors"],
                average_rating=float(book["average_rating"]),
                isbn=book["isbn"],
                isbn13=book["isbn13"],
                language_code=book["language_code"],
                num_pages=int(book["  num_pages"]),
                ratings_count=int(book["ratings_count"]),
                text_reviews_count=int(book["text_reviews_count"]),
                publication_date=datetime.strptime(
                    book["publication_date"], "%m/%d/%Y"
                ).date(),
                publisher=book["publisher"],
                quantity=random.randint(1, 10),
                rent=random.randint(50, 100),
            )
            new_book.book_id = book["bookID"]
            db.session.add(new_book)
        else:
            skipped_book_count += 1
    try:
        db.session.commit()
        if skipped_book_count == 0:
            flash(
                (f"{len(books)} books were added.",),
                category="success",
            )
        elif skipped_book_count == len(books):
            flash(
                ("All books got from API were already in the database.",),
                category="warning",
            )
        else:
            flash(
                (
                    f"Got total {len(books)} books data from API, "
                    f"{len(books) - skipped_book_count} book(s) were added "
                    f"and {skipped_book_count} of them were already in the database.",
                ),
                category="success",
            )
    except:
        flash(
            ("An error has occured while seeding the database!",),
            category="danger",
        )

    return redirect(url_for("books.index"))
