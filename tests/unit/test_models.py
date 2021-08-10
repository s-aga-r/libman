from datetime import date
from tests import Book, Member


def test_book(book):
    """
    GIVEN a Book model
    WHEN a new Book is added
    THEN check all the fields are defined correctly in db
    """
    # Add
    book_from_db = Book.get_by_id(book.book_id)
    assert book_from_db == book

    # Edit
    book_from_db.update(title="Test Book Updated")
    assert book_from_db.title == "Test Book Updated"

    # Remove
    book_from_db.remove()
    book_from_db = Book.get_by_id(book_from_db.book_id)
    assert book_from_db == None


def test_member(member):
    """
    GIVEN a Member model
    WHEN a new Member is added
    THEN check all the fields are defined correctly in db
    """
    # Add
    member_from_db = Member.get_by_id(member.member_id)
    assert member_from_db == member

    # Edit
    member_from_db.update(last_name="Member Updated")
    assert member_from_db.last_name == "Member Updated"

    # Remove
    member_from_db.remove()
    member_from_db = Member.get_by_id(member_from_db.member_id)
    assert member_from_db == None


def test_transaction(transaction):
    """
    GIVEN a Transaction model
    WHEN a Transaction is added
    THEN check all the fields are defined correctly
    """
    assert transaction.book_id == 1
    assert transaction.member_id == 1
    assert transaction.rent == 100
    assert transaction.issue_date == date.today()
