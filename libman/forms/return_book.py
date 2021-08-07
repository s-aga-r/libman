from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.core import DateField, SelectField
from wtforms.validators import DataRequired


class ReturnBookForm(FlaskForm):
    book_id = SelectField(label="Book", choices=[], validators=[DataRequired()])
    member_id = SelectField(label="Member", choices=[], validators=[DataRequired()])
    return_date = DateField(label="Return Date", validators=[DataRequired()])
    submit = SubmitField(label="Save")
