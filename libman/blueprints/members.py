from flask.helpers import url_for
from werkzeug.utils import redirect
from libman.models import Member
from flask import Blueprint, render_template, request, flash
from flask.blueprints import Blueprint
from libman.forms import AddMemberForm, EditMemberForm
from libman import db

member = Blueprint("members", __name__, url_prefix="/members")


# GET - /members
@member.route("/", methods=["GET"])
def index():
    # Search.
    search = request.args.get("s")
    if search:
        members = db.engine.execute(
            f"SELECT * FROM member WHERE first_name || ' ' || last_name LIKE '%{search}%'"
        )
        flash((f"Search results for : {search}",), category="info")
    else:
        members = Member.query.all()

    return render_template("members/index.html", members=members)


# GET & POST - /members/add
@member.route("/add", methods=["GET", "POST"])
def add():
    form = AddMemberForm()

    # Add member to database.
    if form.validate_on_submit():
        member = Member(first_name=form.first_name.data, last_name=form.last_name.data)
        db.session.add(member)
        db.session.commit()
        flash(
            (f"New member added with Member ID = {member.memberID}.",),
            category="success",
        )
        return redirect(url_for("members.index"))

    # Flash error messages.
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg, category="danger")

    return render_template("members/add.html", form=form)


# POST - /books/remove
@member.route("/remove", methods=["POST"])
def remove():
    # Get member through memberID.
    member = Member.query.filter_by(memberID=request.form.get("memberID")).first()
    message = f"Member with Member ID = {member.memberID} "
    if member:
        db.session.delete(member)
        db.session.commit()
        message += "has been removed."
    else:
        message += "does not found or it has been removed earlier."
    flash(
        (f"{message}",),
        category="warning",
    )
    return redirect(url_for("members.index"))


# GET & POST - /members/edit/<id>
@member.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    form = EditMemberForm()
    member = Member.query.filter_by(memberID=id).first()

    # Update and save member to database.
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

    # Flash error messages.
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg, category="danger")
    else:
        # Set value for form attributes using member instance.
        if member:
            form.memberID.data = member.memberID
            form.first_name.data = member.first_name
            form.last_name.data = member.last_name
            form.outstanding_amount.data = member.outstanding_amount

    return render_template("members/edit.html", form=form, id=id)
