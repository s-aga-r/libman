import pytest
from datetime import date
from tests import Book, Member, Transaction, app as flask_app


# Test for Book(Add, Edit, Remove)
@pytest.fixture(scope="module")
def book():
    new_book = Book(
        title="Test Book",
        authors="Unit Test",
        publisher="Unit Test",
    )
    new_book.add()
    return new_book


# Test for Member(Add, Edit, Remove)
@pytest.fixture(scope="module")
def member():
    new_member = Member(first_name="Test", last_name="Member")
    new_member.add()
    return new_member


# Test for Transcation
@pytest.fixture(scope="module")
def transaction():
    transaction = Transaction(book_id=1, member_id=1, rent=100, issue_date=date.today())
    return transaction


@pytest.fixture
def app():
    yield flask_app


# Test for All routes
@pytest.fixture()
def client(app):
    return app.test_client()
