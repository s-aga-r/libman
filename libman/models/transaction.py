from libman.application import db


class Transaction(db.Model):
    transaction_id = db.Column(db.Integer(), primary_key=True)
    book_id = db.Column(db.Integer(), db.ForeignKey("book.book_id"))
    member_id = db.Column(db.Integer(), db.ForeignKey("member.member_id"))
    rent = db.Column(db.Integer(), nullable=False)
    issue_date = db.Column(db.Date(), nullable=False)
    return_date = db.Column(db.Date(), nullable=True)

    def __init__(self, book_id, member_id, rent, issue_date) -> None:
        self.book_id = book_id
        self.member_id = member_id
        self.rent = rent
        self.issue_date = issue_date

    def __repr__(self) -> str:
        return f"{self.transaction_id}"
