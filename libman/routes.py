from flask import Flask, render_template
from libman.books import book
from libman.members import member
from libman.transactions import transaction

app = Flask(__name__)
app.register_blueprint(book)
app.register_blueprint(member)
app.register_blueprint(transaction)


@app.route("/")
def index():
    return render_template("index.html")
