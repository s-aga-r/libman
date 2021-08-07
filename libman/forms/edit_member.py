from flask_wtf import FlaskForm
from flask_wtf.recaptcha import widgets
from wtforms import StringField, SubmitField
from wtforms.fields.core import IntegerField
from wtforms.validators import Length, DataRequired, NumberRange


class EditMemberForm(FlaskForm):
    memberID = IntegerField(label="Member ID", validators=[DataRequired()])
    first_name = StringField(
        label="First Name", validators=[Length(min=1, max=15), DataRequired()]
    )
    last_name = StringField(
        label="Last Name", validators=[Length(min=1, max=15), DataRequired()]
    )
    outstanding_amount = IntegerField(label="O/S Amount")
    submit = SubmitField(label="Save")
