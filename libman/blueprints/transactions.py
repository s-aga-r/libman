from flask.helpers import url_for
from werkzeug.utils import redirect
from libman.models.transaction import Transaction
import flask
from flask.blueprints import Blueprint
from flask import Blueprint, render_template, flash
from werkzeug.wrappers import request
from libman.forms import IssueBookForm
from libman.models import Book, Member
from libman import db

transaction = Blueprint("transactions", __name__, url_prefix="/transactions")


# GET - /transactions
@transaction.route("/")
def index():
    transactions = Transaction.query.all()
    return render_template("transactions/index.html", transactions=transactions)


# GET & POST - /transactions/issue-book
@transaction.route("/issue-book", methods=["GET", "POST"])
def issue_book():
    form = IssueBookForm()

    if form.validate_on_submit():
        # Get selected book and member by their id's.
        book = Book.query.filter_by(book_id=form.book_id.data).first()
        member = Member.query.filter_by(member_id=form.member_id.data).first()

        # Check for outstanding amount of selected member.
        if member.outstanding_amount + book.rent <= 500:
            book.member_id = member.member_id
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
@transaction.route("/return-book")
def return_book():
    return render_template("transactions/return-book.html")
