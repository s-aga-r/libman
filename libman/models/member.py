from libman import db


class Member(db.Model):
    memberID = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    outstanding_amount = db.Column(db.Integer(), nullable=False, default=0)
    books = db.relationship("Book", backref="owned_member", lazy=True)

    def __init__(self, first_name, last_name) -> None:
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self) -> str:
        return f"{self.first_name} {self.last_name}"
