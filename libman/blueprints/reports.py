import io
from flask.blueprints import Blueprint
from flask.templating import render_template
from flask import send_file, Response
from libman.models import Book, Member, Transaction
import docraptor

report = Blueprint("reports", __name__, url_prefix="/reports")


# GET - /<name>
@report.route("/<name>", methods=["GET"])
def index(name):
    if name == "books":
        books = Book.query.all()
        return render_template("reports/books.html", books=books)
    if name == "members":
        members = Member.query.all()
        return render_template("reports/members.html", members=members)
    if name == "transactions":
        transactions = Transaction.query.all()
        return render_template("reports/transactions.html", transactions=transactions)

    return Response(status=404)


# GET - /reports/download/<name>
@report.route("/download/<name>", methods=["GET"])
def download(name):
    if name == "books":
        books = Book.query.all()
        rendered = render_template("reports/books-download.html", books=books)
    elif name == "members":
        members = Member.query.all()
        rendered = render_template("reports/members-download.html", members=members)
    elif name == "transactions":
        transactions = Transaction.query.all()
        rendered = render_template(
            "reports/transactions-download.html", transactions=transactions
        )
    else:
        return Response(status=404)

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

    return send_file(
        path_or_file=io.BytesIO(response),
        mimetype="application/pdf",
        as_attachment=True,
        attachment_filename=f"{name}-report.pdf",
        cache_timeout=-1,
    )
