from flask.helpers import url_for
from werkzeug.utils import redirect
from libman.models.transaction import Transaction
from flask.blueprints import Blueprint
from flask import Blueprint, render_template, flash
from libman.forms import IssueBookForm, ReturnBookForm
from libman.models import Book, Member
from libman import db

transaction = Blueprint("transactions", __name__, url_prefix="/transactions")


# GET - /transactions
@transaction.route("/")
def index():
    transactions = Transaction.query.all()
    books_id = [transaction.book_id for transaction in transactions]
    members_id = [transaction.member_id for transaction in transactions]
    books = {
        book.book_id: book.title
        for book in Book.query.all()
        if book.book_id in books_id
    }
    members = {
        member.member_id: member.first_name + " " + member.last_name
        for member in Member.query.all()
        if member.member_id in members_id
    }
    return render_template(
        "transactions/index.html",
        transactions=transactions,
        books=books,
        members=members,
    )


# GET & POST - /transactions/issue-book
@transaction.route("/issue-book", methods=["GET", "POST"])
def issue_book():
    form = IssueBookForm()
    available_books = [
        (book.book_id, book.title)
        for book in Book.query.filter(Book.quantity > 0).all()
    ]
    members = [
        (member.member_id, member.first_name + " " + member.last_name)
        for member in Member.query.all()
    ]
    form.book_id.choices = available_books
    form.member_id.choices = members

    if form.validate_on_submit():
        # Get selected book and member by their id.
        book = Book.query.filter_by(book_id=form.book_id.data).first()
        member = Member.query.filter_by(member_id=form.member_id.data).first()

        # Check for outstanding amount of selected member.
        if member.outstanding_amount + book.rent <= 500:
            book.quantity -= 1
            member.outstanding_amount += book.rent
            transaction = Transaction(
                book_id=book.book_id,
                member_id=member.member_id,
                rent=book.rent,
                issue_date=form.issue_date.data,
            )
            db.session.add(transaction)
            db.session.commit()

            flash(
                (
                    f"Book '{book.title}' with Book ID = {book.book_id} "
                    f"is issued to member '{member.first_name} {member.last_name}' with Member ID = {member.member_id}",
                ),
                category="success",
            )

            return redirect(url_for("transactions.index"))
        else:
            flash(
                (
                    f"Member '{member.first_name} {member.last_name}' with Member ID = {member.member_id} "
                    f"has an outstanding amount of {member.outstanding_amount}.",
                ),
                category="warning",
            )

    return render_template("transactions/issue-book.html", form=form)


# GET & POST - /transactions/return-book
@transaction.route("/return-book", methods=["GET", "POST"])
def return_book():
    form = ReturnBookForm()

    transactions = Transaction.query.filter_by(return_date=None)
    books_id = [transaction.book_id for transaction in transactions]
    members_id = [transaction.member_id for transaction in transactions]
    books = [
        (book.book_id, book.title)
        for book in Book.query.all()
        if book.book_id in books_id
    ]
    members = [
        (member.member_id, member.first_name + " " + member.last_name)
        for member in Member.query.all()
        if member.member_id in members_id
    ]
    form.book_id.choices = books
    form.member_id.choices = members

    if form.validate_on_submit():
        book = Book.query.filter_by(book_id=form.book_id.data).first()
        member = Member.query.filter_by(member_id=form.member_id.data).first()
        transaction = Transaction.query.filter(
            Transaction.book_id == book.book_id,
            Transaction.member_id == member.member_id,
            Transaction.return_date == None,
        ).first()

        if transaction:
            book.quantity += 1
            member.outstanding_amount -= transaction.rent
            transaction.return_date = form.return_date.data
            db.session.commit()

            flash(
                (
                    f"Book '{book.title}' with Book ID '{book.book_id}' "
                    "was returned by member "
                    f"'{member.first_name} {member.last_name}' with Member ID = {member.member_id}.",
                ),
                category="success",
            )
            return redirect(url_for("transactions.index"))
        else:
            flash(
                (
                    f"Selected book '{book.title}' with Book ID = {book.book_id} "
                    "does not belongs to selected member "
                    f"'{member.first_name} {member.last_name}' with Member ID = {member.member_id}",
                ),
                category="warning",
            )

    return render_template("transactions/return-book.html", form=form)


# GET - /transactions/member/<id>
@transaction.route("/member/<id>")
def member_transactions(id):
    pass
