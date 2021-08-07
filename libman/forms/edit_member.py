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

    def validate_outstanding_amount(self, outstanding_amount):
        if outstanding_amount.data < 0 or outstanding_amount.data > 500:
            raise ValidationError(
                "Outstanding Amount must be less than or equal to 500."
            )
