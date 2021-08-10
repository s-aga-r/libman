from libman import db
import random
from datetime import date


class Book(db.Model):
    book_id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    authors = db.Column(db.String(), nullable=False)
    average_rating = db.Column(db.Float(), nullable=False)
    isbn = db.Column(db.String(), nullable=False, unique=True)
    isbn13 = db.Column(db.String(), nullable=False, unique=True)
    language_code = db.Column(db.String(), nullable=False)
    num_pages = db.Column(db.Integer(), nullable=False)
    ratings_count = db.Column(db.Integer(), nullable=False)
    text_reviews_count = db.Column(db.Integer(), nullable=False)
    publication_date = db.Column(db.Date(), nullable=False)
    publisher = db.Column(db.String(), nullable=False)
    quantity = db.Column(db.Integer(), nullable=False, default=random.randint(1, 10))
    rent = db.Column(db.Integer(), nullable=False, default=random.randint(50, 100))
    transactions = db.relationship("Transaction", backref="book", lazy=True)

    def __init__(
        self,
        title=None,
        authors=None,
        average_rating=None,
        isbn=None,
        isbn13=None,
        language_code=None,
        num_pages=None,
        ratings_count=None,
        text_reviews_count=None,
        publication_date=None,
        publisher=None,
        quantity=None,
        rent=None,
    ) -> None:
        self.title = title if title else "Untitled"
        self.authors = authors if authors else "Undefined"
        self.average_rating = (
            average_rating if average_rating else round(random.uniform(1, 5), 1)
        )
        self.isbn = isbn if isbn else random.randrange(1000000000, 10000000000)
        self.isbn13 = (
            isbn13 if isbn13 else random.randrange(1000000000000, 10000000000000)
        )
        self.language_code = (
            language_code
            if language_code
            else random.choice(["eng", "spa", "en-GB", "en-US", "ger", "enm"])
        )
        self.num_pages = num_pages if num_pages else random.randint(1, 1000)
        self.ratings_count = ratings_count if ratings_count else random.randint(1, 1000)
        self.text_reviews_count = (
            text_reviews_count if text_reviews_count else random.randint(1, 1000)
        )
        self.publication_date = publication_date if publication_date else date.today()
        self.publisher = publisher if publisher else "Undefined"
        self.quantity = quantity if quantity else random.randint(1, 10)
        self.rent = rent if rent else random.randint(50, 100)

    def __repr__(self) -> str:
        return f"{self.title}"

    def add(self) -> None:
        db.session.add(self)
        db.session.commit()

    def remove(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def update(
        self,
        title=None,
        authors=None,
        average_rating=None,
        isbn=None,
        isbn13=None,
        language_code=None,
        num_pages=None,
        ratings_count=None,
        text_reviews_count=None,
        publication_date=None,
        publisher=None,
        quantity=None,
        rent=None,
    ) -> None:
        self.title = title if title else self.title
        self.authors = authors if authors else self.authors
        self.average_rating = average_rating if average_rating else self.average_rating
        self.isbn = isbn if isbn else self.isbn
        self.isbn13 = isbn13 if isbn13 else self.isbn13
        self.language_code = language_code if language_code else self.language_code
        self.num_pages = num_pages if num_pages else self.num_pages
        self.ratings_count = ratings_count if ratings_count else self.ratings_count
        self.text_reviews_count = (
            text_reviews_count if text_reviews_count else self.text_reviews_count
        )
        self.publication_date = (
            publication_date if publication_date else self.publication_date
        )
        self.publisher = publisher if publisher else self.publisher
        self.quantity = quantity if quantity else self.quantity
        self.rent = rent if rent else self.rent
        db.session.commit()

    def issue(self, member, transaction) -> None:
        self.quantity -= 1
        member.outstanding_amount += self.rent
        db.session.add(transaction)
        db.session.commit()

    def issue_return(self, member, transaction) -> None:
        self.quantity += 1
        member.outstanding_amount -= transaction.rent
        db.session.commit()

    @staticmethod
    def search_by(search) -> list[object]:
        return Book.query.filter(
            (Book.title + " " + Book.authors).like(f"%{search}%")
        ).all()

    @staticmethod
    def get_by_id(id) -> object:
        return Book.query.filter_by(book_id=id).first()

    @staticmethod
    def books_in_stock() -> list[object]:
        return [
            (book.book_id, book.title)
            for book in Book.query.filter(Book.quantity > 0).all()
        ]
