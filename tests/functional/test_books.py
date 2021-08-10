# url - /books/
def test_index_page(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/books' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get("/books/")
    assert response.status_code == 200
    assert b"Books" in response.data
    assert b"Add Book" in response.data
    assert b"Search" in response.data


# url - /books/add
def test_add_page(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/books/add' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get("/books/add")
    assert response.status_code == 200
    assert b"Add Book" in response.data
    assert b"Title" in response.data
    assert b"Authors" in response.data


# url - /books/edit/<id>
def test_details_page(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/books/details/<id>' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get("/books/details/0")
    assert response.status_code == 302


# url - /books/edit/<id>
def test_edit_page(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/books/edit/<id>' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get("/books/edit/0")
    assert response.status_code == 302
