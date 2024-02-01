def test_get_records(client):
    response = client.get("/records")
    assert response.status_code == 200
    assert "oai:FakeArXiv.org:1234.5678" in response.json["records"]
    assert "oai:FakeArXiv.org:2345.6789" in response.json["records"]
    assert "oai:FakeArXiv.org:3456.7890" in response.json["records"]


def test_get_records_with_limit(client):
    response = client.get("/records?limit=2")
    assert response.status_code == 200
    assert len(response.json["records"]) == 2


def test_get_records_with_zero_limit(client):
    response = client.get("/records?limit=0")
    assert response.status_code == 200
    assert len(response.json["records"]) == 0


def test_get_records_with_negative_limit(client):
    response = client.get("/records?limit=-1")
    assert response.status_code == 400


def test_get_records_with_non_integer_limit(client):
    response = client.get("/records?limit=abc")
    assert response.status_code == 400


def test_get_records_with_category(client):
    response = client.get("/records?category=Computer Science - Fake Subject")
    assert response.status_code == 200
    assert "oai:FakeArXiv.org:1234.5678" in response.json["records"]
    assert "oai:FakeArXiv.org:2345.6789" in response.json["records"]


def test_get_records_with_wrong_category(client):
    response = client.get("/records?category=wrong_category")
    assert response.status_code == 200
    assert response.json == {"records": []}


def test_get_records_with_author(client):
    response = client.get("/records?author=Fake, Author A.")
    assert response.status_code == 200
    assert "oai:FakeArXiv.org:1234.5678" in response.json["records"]


def test_get_records_with_wrong_author(client):
    response = client.get("/records?author=Wrong, Author")
    assert response.status_code == 200
    assert response.json == {"records": []}


def test_get_records_with_date(client):
    response = client.get("/records?date=2022-01-02")
    assert response.status_code == 200
    assert "oai:FakeArXiv.org:1234.5678" in response.json["records"]
    assert "oai:FakeArXiv.org:2345.6789" in response.json["records"]


def test_get_records_with_one_date(client):
    response = client.get("/records?date=2022-01-05")
    assert response.status_code == 200
    assert "oai:FakeArXiv.org:3456.7890" in response.json["records"]


def test_get_records_with_wrong_date(client):
    response = client.get("/records?date=2022-01-06")
    assert response.status_code == 200
    assert response.json == {"records": []}
