# url - /members/
def test_index_page(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/members/' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get("/members/")
    assert response.status_code == 200
    assert b"Members" in response.data
    assert b"Add Member" in response.data
    assert b"Search" in response.data


# url - /members/add
def test_add_page(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/members/add' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get("/members/add")
    assert response.status_code == 200
    assert b"Add Member" in response.data
    assert b"First Name" in response.data
    assert b"Last Name" in response.data


# url - /members/edit/<id>
def test_edit_page(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/members/edit/<id>' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get("/members/edit/0")
    assert response.status_code == 302
