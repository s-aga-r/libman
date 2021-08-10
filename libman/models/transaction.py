from datetime import date
from libman.models.member import Member
from libman import db


class Transaction(db.Model):
    transaction_id = db.Column(db.Integer(), primary_key=True)
    book_id = db.Column(db.Integer(), db.ForeignKey("book.book_id"))
    member_id = db.Column(db.Integer(), db.ForeignKey("member.member_id"))
    rent = db.Column(db.Integer(), nullable=False)
    issue_date = db.Column(db.Date(), nullable=False)
    return_date = db.Column(db.Date(), nullable=True)

    def __init__(self, book_id, member_id, rent, issue_date=None) -> None:
        self.book_id = book_id
        self.member_id = member_id
        self.rent = rent
        self.issue_date = issue_date if issue_date else date.today()

    def __repr__(self) -> str:
        return f"{self.transaction_id}"

    @staticmethod
    def search_by_member_name(search) -> list[object]:
        return (
            Transaction.query.join(Transaction.member)
            .filter((Member.first_name + " " + Member.last_name).like(f"%{search}%"))
            .all()
        )

    @staticmethod
    def incomplete_transaction(book_id, member_id) -> object:
        return Transaction.query.filter(
            Transaction.book_id == book_id,
            Transaction.member_id == member_id,
            Transaction.return_date == None,
        ).first()

    @staticmethod
    def incomplete_transactions() -> list[object]:
        return Transaction.query.filter_by(return_date=None)

    @staticmethod
    def member_transactions(member_id) -> list[object]:
        return Transaction.query.filter_by(member_id=member_id).all()

    @staticmethod
    def book_transactions(book_id) -> list[object]:
        return Transaction.query.filter_by(book_id=book_id).all()
