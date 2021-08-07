from flask import Blueprint, jsonify
from libman.models import Transaction, Book

chart = Blueprint("charts", __name__, url_prefix="/charts")


@chart.route("/")
def top_books():

    top_books = {
        "labels": [],
        "values": [],
    }
    stock = {
        "labels": [],
        "values": [],
    }

    for transaction in Transaction.query.all():
        top_books["labels"].append(transaction.book.title)
        top_books["values"].append(transaction.book.book_id)

    for book in Book.query.all():
        stock["labels"].append(book.title)
        stock["values"].append(book.quantity)

    data = {
        "top_books": top_books,
        "stock": stock,
    }

    return jsonify(data)
