def test_get_records(client):
    response = client.get("/records")
    assert response.status_code == 200
    assert (response.json == {"records": ["pytest_test1", "pytest_test2"]}) or (
        response.json == {"records": ["pytest_test2", "pytest_test1"]}
    )


def test_get_records_with_limits(client):
    response = client.get("/records?category=pytest_test&limit=1")
    assert response.status_code == 200
    assert response.json == {"records": ["pytest_test1"]}


def test_get_records_with_category(client):
    response = client.get("/records?category=pytest_test")
    assert response.status_code == 200
    assert response.json == {"records": ["pytest_test1", "pytest_test2"]}


def test_index(app, client):
    res = client.get("/")
    assert res.status_code == 200
    expected = {"hello": "world"}


def test_get_records_with_author(client):
    response = client.get("/records?author=pytest_author")
    assert response.status_code == 200
    assert response.json == {"records": ["pytest_test1", "pytest_test2"]}
