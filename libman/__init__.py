from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///libman.db"
db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")


from libman.blueprints import book, member, transaction

app.register_blueprint(book)
app.register_blueprint(member)
app.register_blueprint(transaction)
