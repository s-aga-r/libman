from libman import db


class Transaction(db.Model):
    transactionID = db.Column(db.Integer(), primary_key=True)
    bookID = db.Column(db.Integer(), db.ForeignKey("book.bookID"))
    memberID = db.Column(db.Integer(), db.ForeignKey("member.memberID"))
    issue_date = db.Column(db.Date(), nullable=False)
    returned_date = db.Column(db.Date(), nullable=True)

    def __init__(self, bookID, memberID, issue_date) -> None:
        self.bookID = bookID
        self.memberID = memberID
        self.issue_date = issue_date

    def __repr__(self) -> str:
        return f"{self.transactionID}"
