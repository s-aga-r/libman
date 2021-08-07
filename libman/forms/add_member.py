from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, DataRequired


class AddMemberForm(FlaskForm):
    first_name = StringField(
        label="First Name", validators=[Length(min=1, max=15), DataRequired()]
    )
    last_name = StringField(
        label="Last Name", validators=[Length(min=1, max=15), DataRequired()]
    )
    submit = SubmitField(label="Save")
