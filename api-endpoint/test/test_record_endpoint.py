def test_get_records(client):
    response = client.get("/records")
    assert response.status_code == 200
    assert (response.json == {"records": ["pytest_test1", "pytest_test2"]}) or (
        response.json == {"records": ["pytest_test2", "pytest_test1"]}
    )


def test_get_records_with_limit_0(client):
    response = client.get("/records?category=pytest_test&limit=0")
    assert response.status_code == 200
    assert response.json == {"records": []}


def test_get_records_with_limit_1(client):
    response = client.get("/records?category=pytest_test&limit=1")
    assert response.status_code == 200
    assert response.json == {"records": ["pytest_test1"]}


def test_get_records_with_limit_2(client):
    response = client.get("/records?category=pytest_test&limit=2")
    assert response.status_code == 200
    assert response.json == {"records": ["pytest_test1", "pytest_test2"]}


def test_get_records_with_category(client):
    response = client.get("/records?category=pytest_test")
    assert response.status_code == 200
    assert response.json == {"records": ["pytest_test1", "pytest_test2"]}


def test_get_records_with_wrong_category(client):
    response = client.get("/records?category=pytest_wrong_test")
    assert response.status_code == 200
    assert response.json == {"records": []}


def test_index(app, client):
    res = client.get("/")
    assert res.status_code == 200
    expected = {"hello": "world"}


def test_get_records_with_author(client):
    response = client.get("/records?author=pytest_author")
    assert response.status_code == 200
    assert response.json == {"records": ["pytest_test1", "pytest_test2"]}


def test_get_records_with_wrong_author(client):
    response = client.get("/records?author=pytest_wrong_author")
    assert response.status_code == 200
    assert response.json == {"records": []}


def test_get_records_with_date(client):
    response = client.get("/records?date=2022-01-01")
    assert response.status_code == 200
    assert response.json == {"records": ["pytest_test1"]}


def test_get_records_with_wront_date(client):
    response = client.get("/records?date=2022-01-03")
    assert response.status_code == 200
    assert response.json == {"records": []}
