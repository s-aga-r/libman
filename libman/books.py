from flask.blueprints import Blueprint


from flask import Blueprint, render_template

book = Blueprint("books", __name__, url_prefix="/books")


@book.route("/")
def index():
    return render_template("book/index.html")
