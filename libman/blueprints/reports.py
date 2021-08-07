import io
from flask.blueprints import Blueprint
from flask.helpers import flash, url_for
from flask.templating import render_template
import pdfkit as pdf
from flask import send_file
from werkzeug.utils import redirect
from libman.models import Book, Member, Transaction

report = Blueprint("reports", __name__, url_prefix="/reports")


# GET - /reports/books
@report.route("/books", methods=["GET"])
def books_report():
    books = Book.query.all()
    rendered = render_template("reports/books.html", books=books)

    try:
        file = io.BytesIO(pdf.from_string(input=rendered, output_path=False))
    except:
        flash(("wkhtmltopdf is missing.",), category="danger")
        return redirect(url_for("index"))
    else:
        filename = f"books-report.pdf"

        return send_file(
            path_or_file=file,
            mimetype="application/pdf",
            as_attachment=True,
            attachment_filename=filename,
            cache_timeout=-1,
        )


# GET - /reports/members
@report.route("/members", methods=["GET"])
def members_report():
    members = Member.query.all()
    rendered = render_template("reports/members.html", members=members)

    try:
        file = io.BytesIO(pdf.from_string(input=rendered, output_path=False))
    except:
        flash(("wkhtmltopdf is missing.",), category="danger")
        return redirect(url_for("index"))
    else:
        filename = f"members-report.pdf"

        return send_file(
            path_or_file=file,
            mimetype="application/pdf",
            as_attachment=True,
            attachment_filename=filename,
            cache_timeout=-1,
        )


# GET - /reports/transactions
@report.route("/transactions", methods=["GET"])
def transactions_report():
    transactions = Transaction.query.all()
    rendered = render_template("reports/transactions.html", transactions=transactions)
    options = {
        "page-size": "A2",
    }

    try:
        file = io.BytesIO(
            pdf.from_string(input=rendered, output_path=False, options=options)
        )
    except:
        flash(("wkhtmltopdf is missing.",), category="danger")
        return redirect(url_for("index"))
    else:
        filename = f"transactions-report.pdf"

        return send_file(
            path_or_file=file,
            mimetype="application/pdf",
            as_attachment=True,
            attachment_filename=filename,
            cache_timeout=-1,
        )
