from flask.helpers import url_for
from werkzeug.utils import redirect
from libman.models import Member
from flask import Blueprint, render_template, request, flash
from flask.blueprints import Blueprint
from libman.forms import AddMemberForm, EditMemberForm

member = Blueprint("members", __name__, url_prefix="/members")


# GET - /members
@member.route("/", methods=["GET"])
def index():

    # Search.
    search = request.args.get("s")

    if search:
        members = Member.search_by(search)
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
        member.add()

        flash(
            (f"Member added with Member ID = {member.member_id}.",),
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

    # Get member through member_id.
    member = Member.get_by_id(request.form.get("member_id"))
    message = f"Member with Member ID = {member.member_id} "

    if member:
        member.remove()
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
    member = Member.get_by_id(id)

    # Update and save member to database.
    if form.validate_on_submit():
        member.update(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
        )

        flash(
            (f"Member updated with Member ID = {form.member_id.data}.",),
            category="success",
        )

        return redirect(url_for("members.index"))

    # Flash error messages.
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg, category="danger")
    else:
        # Initialize form fields with member object.
        if member:
            form.fill_data(member)
        else:
            flash(("Member not found!",), category="warning")
            return redirect(url_for("members.index"))
    return render_template("members/edit.html", form=form, id=id)
