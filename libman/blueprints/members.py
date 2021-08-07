from flask.helpers import url_for
from werkzeug.utils import redirect
from libman.models import Member
from flask import Blueprint, render_template, request, flash
from flask.blueprints import Blueprint
from libman.forms import AddMemberForm, EditMemberForm
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


@member.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    form = EditMemberForm()
    member = Member.query.filter_by(memberID=id).first()

    if form.validate_on_submit():
        member.first_name = form.first_name.data
        member.last_name = form.last_name.data
        member.outstanding_amount = form.outstanding_amount.data
        db.session.commit()

        flash(
            (f"Member updated with Member ID = {form.memberID.data}.",),
            category="success",
        )
        return redirect(url_for("members.index"))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg, category="danger")
    else:
        if member:
            form.memberID.data = member.memberID
            form.first_name.data = member.first_name
            form.last_name.data = member.last_name
            form.outstanding_amount.data = member.outstanding_amount

    return render_template("members/edit.html", form=form, id=id)
