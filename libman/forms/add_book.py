from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.core import DateField, IntegerField
from wtforms.validators import Length, DataRequired


class AddBookForm(FlaskForm):
    title = StringField(label="Title", validators=[Length(min=2), DataRequired()])
    authors = StringField(label="Authors", validators=[Length(min=2), DataRequired()])
    average_rating = StringField(label="Average Rating", validators=[DataRequired()])
    isbn = StringField(
        label="ISBN", validators=[Length(min=10, max=10), DataRequired()]
    )
    isbn13 = StringField(
        label="ISBM13", validators=[Length(min=13, max=13), DataRequired()]
    )
    language_code = StringField(
        label="Language Code", validators=[Length(min=2), DataRequired()]
    )
    num_pages = IntegerField(label="Number of Pages", validators=[DataRequired()])
    ratings_count = IntegerField(label="Ratings Count", validators=[DataRequired()])
    text_reviews_count = IntegerField(
        label="Text Reviews Count", validators=[DataRequired()]
    )
    publication_date = DateField(label="Publication Date", validators=[DataRequired()])
    publisher = StringField(
        label="Publisher", validators=[Length(min=2), DataRequired()]
    )
    rent = IntegerField(label="Rent", validators=[DataRequired()])
    submit = SubmitField(label="Save")
