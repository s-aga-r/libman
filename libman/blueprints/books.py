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
        books = Book.search_by(search)
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
        book.add()

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
        # Initialize form fields with random dummy values.
        form.dummy_data()

    return render_template("books/add.html", form=form)


# POST - /books/remove
@book.route("/remove", methods=["POST"])
def remove():

    # Get book through book_id.
    book = Book.get_by_id(request.form.get("book_id"))
    message = f"Book with Book ID = {book.book_id} "

    if book:
        book.remove()
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
    return render_template("books/details.html", book=Book.get_by_id(id), id=id)


# GET & POST - /books/edit/<id>
@book.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    form = EditBookForm()
    book = Book.get_by_id(id)

    # Update and save book to database.
    if form.validate_on_submit():
        book.update(
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
        # Initialize form fields with book object.
        if book:
            form.fill_data(book)

    return render_template("books/edit.html", form=form, id=id)


# POST - /books/seed
@book.route("/seed", methods=["POST"])
def seed():
    response = requests.get("https://frappe.io/api/method/frappe-library")
    json_response = response.json()
    books = list(json_response["message"])

    # Get existing book title in a list.
    existing_books_title = []
    for book_title in db.session.query(Book.title).all():
        existing_books_title.append(book_title[0])

    skipped_book_count = 0
    for book in books:
        # Only add those books, which are not available in the database.
        if book["title"] not in existing_books_title:
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
