from libman.models.member import Member
from flask import Blueprint, jsonify
from libman.models import Transaction, Book
from libman.application import db
from sqlalchemy import func

chart = Blueprint("charts", __name__, url_prefix="/charts")


@chart.route("/")
def top_books():
    def popular_books(top=10):
        # Get books data from db.
        books_data = (
            db.session.query(Book.title, func.count(Transaction.book_id), Book.quantity)
            .join(Book)
            .group_by(Transaction.book_id)
            .all()
        )

        # Sort by no. of transaction in desc order
        books_data.sort(key=lambda item: item[1], reverse=True)

        # Get top 10 records from sorted list 'books_data'
        books_data = books_data[:top]

        books = {
            "title": [],
            "no_of_transaction": [],
            "quantity": [],
        }

        for book_data in books_data:
            books["title"].append(book_data[0])
            books["no_of_transaction"].append(book_data[1])
            books["quantity"].append(book_data[2])

        return books

    def highest_paying_members(top=10):
        # Get members data from db.
        members_data = (
            db.session.query(
                Member.first_name + " " + Member.last_name,
                func.count(Transaction.member_id),
                func.sum(Transaction.rent),
            )
            .join(Member)
            .group_by(Transaction.member_id)
            .all()
        )

        # Sort by amount received in desc order
        members_data.sort(key=lambda item: item[2], reverse=True)

        # Get top 10 records from sorted list 'members_data'
        members_data = members_data[:top]

        members = {
            "name": [],
            "no_of_transaction": [],
            "amount": [],
        }

        for member_data in members_data:
            members["name"].append(member_data[0])
            members["no_of_transaction"].append(member_data[1])
            members["amount"].append(member_data[2])

        return members

    data = {
        "books": popular_books(),
        "members": highest_paying_members(),
    }

    return jsonify(data)
