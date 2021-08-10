# url - /transactions/
def test_index_page(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/transactions/' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get("/transactions/")
    assert response.status_code == 200
    assert b"Transactions" in response.data


# url - /transactions/issue-book
def test_issue_page(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/transactions/issue-book' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get("/transactions/issue-book")
    assert response.status_code == 200
    assert b"Book Issue" in response.data
    assert b"Issue Date" in response.data
