from datetime import date, datetime
from flask.helpers import url_for
from werkzeug.utils import redirect
from libman.models.transaction import Transaction
from flask.blueprints import Blueprint
from flask import Blueprint, render_template, flash, request
from libman.forms import IssueBookForm, ReturnBookForm
from libman.models import Book, Member, member
from libman.application import db

transaction = Blueprint("transactions", __name__, url_prefix="/transactions")


# GET - /transactions
@transaction.route("/", methods=["GET"])
def index():

    # Search.
    search = request.args.get("s")

    if search:
        transactions = Transaction.search_by_member_name(search)
        flash((f"Search results for : {search}",), category="info")
    else:
        transactions = Transaction.query.all()

    # Sort.
    sort_by = request.args.get(key="sort-by")

    if sort_by == "issue-date":
        transactions.sort(key=lambda transaction: transaction.issue_date)
        flash(("Sort by : Issue Date",), category="info")
    elif sort_by == "return-date":

        def sort_by_return_date(transaction):
            if isinstance(transaction.return_date, date):
                return transaction.return_date
            # If book is not return yet.
            return date.today()

        transactions.sort(key=sort_by_return_date)
        flash(("Sort by : Return Date",), category="info")

    return render_template(
        "transactions/index.html", transactions=transactions, show_filters=True
    )


# GET & POST - /transactions/issue-book
@transaction.route("/issue-book", methods=["GET", "POST"])
def issue_book():
    form = IssueBookForm()

    # Set options for dropdown list.
    form.book_id.choices = Book.books_in_stock()
    form.member_id.choices = Member.members()

    if form.validate_on_submit():
        # Get selected book and member by their id.
        book = Book.get_by_id(form.book_id.data)
        member = Member.get_by_id(form.member_id.data)

        # Check for outstanding amount of selected member.
        if member.outstanding_amount + book.rent <= 500:
            transaction = Transaction(
                book_id=book.book_id,
                member_id=member.member_id,
                rent=book.rent,
                issue_date=form.issue_date.data,
            )
            book.issue(member, transaction)

            flash(
                (
                    f"Book '{book}' with Book ID = {book.book_id} "
                    f"is issued to member '{member}' with Member ID = {member.member_id}",
                ),
                category="success",
            )

            return redirect(url_for("transactions.index"))
        else:
            flash(
                (
                    f"Member '{member}' with Member ID = {member.member_id} "
                    f"has an outstanding amount of {member.outstanding_amount}.",
                ),
                category="warning",
            )

    return render_template("transactions/issue-book.html", form=form)


# GET & POST - /transactions/return-book
@transaction.route("/return-book", methods=["GET", "POST"])
def return_book():
    form = ReturnBookForm()

    transactions = Transaction.incomplete_transactions()
    books = []
    members = []
    for transaction in transactions:
        books.append((transaction.book.book_id, transaction.book.title))
        members.append(
            (
                transaction.member.member_id,
                transaction.member.first_name + " " + transaction.member.last_name,
            )
        )

    def remove_duplicates(lst):
        return [t for t in (set(tuple(i) for i in lst))]

    form.book_id.choices = remove_duplicates(books)
    form.member_id.choices = remove_duplicates(members)

    if form.validate_on_submit():
        book = Book.get_by_id(form.book_id.data)
        member = Member.get_by_id(form.member_id.data)
        transaction = Transaction.incomplete_transaction(
            book_id=book.book_id, member_id=member.member_id
        )

        if transaction:
            transaction.return_date = form.return_date.data
            book.issue_return(member, transaction)

            flash(
                (
                    f"Book '{book}' with Book ID '{book.book_id}' "
                    "was returned by member "
                    f"'{member}' with Member ID = {member.member_id}.",
                ),
                category="success",
            )

            return redirect(url_for("transactions.index"))
        else:
            flash(
                (
                    f"Selected book '{book}' with Book ID = {book.book_id} "
                    "does not belongs to selected member "
                    f"'{member}' with Member ID = {member.member_id}",
                ),
                category="warning",
            )

    return render_template("transactions/return-book.html", form=form)


# GET - /transactions/member/<id>
@transaction.route("/member/<id>", methods=["GET"])
def member_transactions(id):
    member = Member.get_by_id(id)

    if member:
        transactions = Transaction.member_transactions(member_id=id)

        if transactions:
            flash(
                (
                    f"All transactions of member '{member}' with Member ID = {member.member_id}.",
                ),
                category="info",
            )
        else:
            flash(
                (
                    f"Member '{member}' with Member ID = {member.member_id} has no transactions.",
                ),
                category="info",
            )

        return render_template(
            "transactions/index.html", transactions=transactions, show_filters=False
        )
    else:
        flash(("Member not found!",), category="warning")

    return redirect(url_for("transactions.index"))


# GET - /transactions/book/<id>
@transaction.route("/book/<id>", methods=["GET"])
def book_transactions(id):
    book = Book.get_by_id(id)

    if book:
        transactions = Transaction.book_transactions(book_id=id)

        if transactions:
            flash(
                (f"All transactions for book '{book}' with Book ID = {book.book_id}.",),
                category="info",
            )
        else:
            flash(
                (f"Book '{book}' with Book ID = {book.book_id} has no transactions.",),
                category="info",
            )

        return render_template(
            "transactions/index.html", transactions=transactions, show_filters=False
        )
    else:
        flash(("Book not found!",), category="warning")

    return redirect(url_for("transactions.index"))
