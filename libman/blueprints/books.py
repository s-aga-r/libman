from flask.blueprints import Blueprint
from flask import Blueprint, render_template, request, flash, redirect, url_for
from libman.models import Book
from libman import db
from libman.forms import AddBookForm
import random

book = Blueprint("books", __name__, url_prefix="/books")


# GET - /books
@book.route("/", methods=["GET"])
def index():

    # Search.
    search = request.args.get("s")
    if search:
        books = db.engine.execute(
            f"SELECT * FROM book WHERE title || ' ' || authors LIKE '%{search}%'"
        )
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
            rent=form.rent.data,
        )
        db.session.add(book)
        db.session.commit()
        flash(
            (f"New book added with Book ID = {book.bookID}.",),
            category="success",
        )
        return redirect(url_for("books.index"))

    # Flash error messages.
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg, category="danger")
    else:
        form.average_rating.data = round(random.uniform(1, 5), 1)
        form.language_code.data = random.choice(
            ["eng", "spa", "en-GB", "en-US", "ger", "enm"]
        )
        form.num_pages.data = random.randint(1, 1000)
        form.ratings_count.data = random.randint(1, 1000)
        form.text_reviews_count.data = random.randint(1, 1000)
        form.rent.data = random.randint(50, 100)

    return render_template("books/add.html", form=form)


# POST - /books/remove
@book.route("/remove", methods=["POST"])
def remove():
    # Get book through bookID.
    book = Book.query.filter_by(bookID=request.form.get("bookID")).first()
    message = f"Book with Book ID = {book.bookID} "
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
    book = Book.query.filter_by(bookID=id).first()
    return render_template("books/details.html", book=book, id=id)
