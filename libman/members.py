from flask.blueprints import Blueprint


from flask import Blueprint, render_template

member = Blueprint("members", __name__, url_prefix="/members")


@member.route("/")
def index():
    return render_template("member/index.html")
