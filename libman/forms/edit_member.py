from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.core import IntegerField
from wtforms.validators import Length, DataRequired, ValidationError


class EditMemberForm(FlaskForm):
    member_id = IntegerField(label="Member ID", validators=[DataRequired()])
    first_name = StringField(
        label="First Name", validators=[Length(min=1, max=15), DataRequired()]
    )
    last_name = StringField(
        label="Last Name", validators=[Length(min=1, max=15), DataRequired()]
    )
    outstanding_amount = IntegerField(label="O/S Amount")
    submit = SubmitField(label="Save")

    def fill_data(self, member):
        self.member_id.data = member.member_id
        self.first_name.data = member.first_name
        self.last_name.data = member.last_name
        self.outstanding_amount.data = member.outstanding_amount
