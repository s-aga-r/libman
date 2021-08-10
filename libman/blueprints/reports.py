import io
from flask.blueprints import Blueprint
from flask.templating import render_template
from flask import send_file
from libman.models import Book, Member, Transaction
import docraptor

report = Blueprint("reports", __name__, url_prefix="/reports")


def generate_pdf(rendered):
    doc_api = docraptor.DocApi()
    doc_api.api_client.configuration.username = "T18fkUXD7ZnvSe7DLvEF"

    response = doc_api.create_doc(
        {
            "test": True,
            "document_content": rendered,
            "name": "untitled.pdf",
            "document_type": "pdf",
            "javascript": True,
            "prince_options": {
                "media": "screen",
                "baseurl": "http://127.0.0.1:5000/",
            },
        }
    )

    return io.BytesIO(response)


# GET - /reports/books
@report.route("/books", methods=["GET"])
def books_report():
    books = Book.query.all()
    rendered = render_template("reports/books.html", books=books)

    return send_file(
        path_or_file=generate_pdf(rendered),
        mimetype="application/pdf",
        as_attachment=True,
        attachment_filename="books-report.pdf",
        cache_timeout=-1,
    )


# GET - /reports/members
@report.route("/members", methods=["GET"])
def members_report():
    members = Member.query.all()
    rendered = render_template("reports/members.html", members=members)

    return send_file(
        path_or_file=generate_pdf(rendered),
        mimetype="application/pdf",
        as_attachment=True,
        attachment_filename="members-report.pdf",
        cache_timeout=-1,
    )


# GET - /reports/transactions
@report.route("/transactions", methods=["GET"])
def transactions_report():
    transactions = Transaction.query.all()
    rendered = render_template("reports/transactions.html", transactions=transactions)

    return send_file(
        path_or_file=generate_pdf(rendered),
        mimetype="application/pdf",
        as_attachment=True,
        attachment_filename="transactions-report.pdf",
        cache_timeout=-1,
    )
