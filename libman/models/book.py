from libman.application import db
import random


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
        title,
        authors,
        average_rating,
        isbn,
        isbn13,
        language_code,
        num_pages,
        ratings_count,
        text_reviews_count,
        publication_date,
        publisher,
        quantity,
        rent,
    ) -> None:
        self.title = title
        self.authors = authors
        self.average_rating = average_rating
        self.isbn = isbn
        self.isbn13 = isbn13
        self.language_code = language_code
        self.num_pages = num_pages
        self.ratings_count = ratings_count
        self.text_reviews_count = text_reviews_count
        self.publication_date = publication_date
        self.publisher = publisher
        self.quantity = quantity
        self.rent = rent

    def __repr__(self) -> str:
        return f"{self.title}"

    def add(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def update(
        self,
        title,
        authors,
        average_rating,
        isbn,
        isbn13,
        language_code,
        num_pages,
        ratings_count,
        text_reviews_count,
        publication_date,
        publisher,
        quantity,
        rent,
    ):
        self.title = title
        self.authors = authors
        self.average_rating = average_rating
        self.isbn = isbn
        self.isbn13 = isbn13
        self.language_code = language_code
        self.num_pages = num_pages
        self.ratings_count = ratings_count
        self.text_reviews_count = text_reviews_count
        self.publication_date = publication_date
        self.publisher = publisher
        self.quantity = quantity
        self.rent = rent
        db.session.commit()

    def issue(self, member, transaction):
        self.quantity -= 1
        member.outstanding_amount += self.rent
        db.session.add(transaction)
        db.session.commit()

    def issue_return(self, member, transaction):
        self.quantity += 1
        member.outstanding_amount -= transaction.rent
        db.session.commit()

    @staticmethod
    def search_by(search):
        return Book.query.filter(
            (Book.title + " " + Book.authors).like(f"%{search}%")
        ).all()

    @staticmethod
    def get_by_id(id):
        return Book.query.filter_by(book_id=id).first()

    @staticmethod
    def books_in_stock():
        return [
            (book.book_id, book.title)
            for book in Book.query.filter(Book.quantity > 0).all()
        ]
