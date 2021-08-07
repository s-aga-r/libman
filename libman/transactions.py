from flask.blueprints import Blueprint


from flask import Blueprint, render_template

transaction = Blueprint("transactions", __name__, url_prefix="/transactions")


@transaction.route("/")
def index():
    return render_template("transaction/index.html")
