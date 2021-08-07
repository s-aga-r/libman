from libman.models import Member
from flask import Blueprint, render_template, request
from flask.blueprints import Blueprint

member = Blueprint("members", __name__, url_prefix="/members")


@member.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        members = Member.query.all()
        return render_template("members/index.html", members=members)
