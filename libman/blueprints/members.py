from flask.helpers import url_for
from werkzeug.utils import redirect
from libman.models import Member
from flask import Blueprint, render_template, request, flash
from flask.blueprints import Blueprint
from libman.forms import AddMemberForm
from libman import db

member = Blueprint("members", __name__, url_prefix="/members")


@member.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        members = Member.query.all()
        return render_template("members/index.html", members=members)


@member.route("/add", methods=["GET", "POST"])
def add():
    form = AddMemberForm()

    if form.validate_on_submit():
        member = Member(first_name=form.first_name.data, last_name=form.last_name.data)
        db.session.add(member)
        db.session.commit()
        flash(
            (f"New member added with Member ID = {member.memberID}.",),
            category="success",
        )
        return redirect(url_for("members.index"))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg, category="danger")

    return render_template("members/add.html", form=form)
