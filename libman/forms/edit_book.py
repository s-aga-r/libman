from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.core import DateField, IntegerField
from wtforms.validators import Length, DataRequired, ValidationError
from libman.models import Book


class EditBookForm(FlaskForm):
    book_id = IntegerField(label="Book ID", validators=[DataRequired()])
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
    quantity = IntegerField(label="Quantity", validators=[DataRequired()])
    rent = IntegerField(label="Rent", validators=[DataRequired()])
    submit = SubmitField(label="Save")

    def validate_average_rating(self, average_rating):
        try:
            val = float(average_rating.data)
            if not (val >= 1.0 and val <= 5.0):
                raise ValueError
        except:
            raise ValidationError(
                "Average Rating must be a decimal value between 1.0 to 5.0"
            )

    def validate_isbn(self, isbn):
        if not (isbn.data.isnumeric() and len(isbn.data) == 10):
            raise ValidationError("ISBN must be a number of 10 digits.")
        book = Book.query.filter_by(isbn=isbn.data).first()
        if book and book.book_id != self.book_id.data:
            raise ValidationError("ISBN must be unique for every book.")

    def validate_isbn13(self, isbn13):
        if not (isbn13.data.isnumeric() and len(isbn13.data) == 13):
            raise ValidationError("ISBN13 must be a number of 13 digits.")
        book = Book.query.filter_by(isbn13=isbn13.data).first()
        if book and book.book_id != self.book_id.data:
            raise ValidationError("ISBN13 must be unique for every book.")

    def fill_data(self, book):
        self.book_id.data = book.book_id
        self.title.data = book.title
        self.authors.data = book.authors
        self.average_rating.data = book.average_rating
        self.isbn.data = book.isbn
        self.isbn13.data = book.isbn13
        self.language_code.data = book.language_code
        self.num_pages.data = book.num_pages
        self.ratings_count.data = book.ratings_count
        self.text_reviews_count.data = book.text_reviews_count
        self.publication_date.data = book.publication_date
        self.publisher.data = book.publisher
        self.quantity.data = book.quantity
        self.rent.data = book.rent





