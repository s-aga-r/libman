from libman import db


class Member(db.Model):
    member_id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    outstanding_amount = db.Column(db.Integer(), nullable=False, default=0)
    transactions = db.relationship("Transaction", backref="member", lazy=True)

    def __init__(self, first_name, last_name) -> None:
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def add(self) -> None:
        db.session.add(self)
        db.session.commit()

    def remove(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def update(self, first_name=None, last_name=None) -> None:
        self.first_name = first_name if first_name else self.first_name
        self.last_name = last_name if last_name else self.last_name
        db.session.commit()

    @staticmethod
    def search_by(search) -> list[object]:
        return Member.query.filter(
            (Member.first_name + " " + Member.last_name).like(f"%{search}%")
        ).all()

    @staticmethod
    def get_by_id(id) -> object:
        return Member.query.filter_by(member_id=id).first()

    @staticmethod
    def members() -> list[object]:
        return [
            (member.member_id, member.first_name + " " + member.last_name)
            for member in Member.query.all()
        ]
