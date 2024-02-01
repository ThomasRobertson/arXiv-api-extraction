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


def test_post_records(client):
    get_response = client.get("/records")
    assert get_response.status_code == 200
    assert "oai:arXiv.org:1004.3608" not in get_response.json["records"]

    xml_string = """
    <OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
    <record>
    <header>
     <identifier>oai:arXiv.org:1004.3608</identifier>
     <datestamp>2021-03-22</datestamp>
     <setSpec>cs</setSpec>
    </header>
    <metadata>
     <oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
     <dc:title>Mock Title</dc:title>
     <dc:creator>Mock Creator</dc:creator>
     <dc:subject>Mock Subject</dc:subject>
     <dc:subject>Mock Subject</dc:subject>
     <dc:subject>Mock Subject</dc:subject>
     <dc:subject>Mock Subject</dc:subject>
     <dc:subject>Mock Subject</dc:subject>
     <dc:description>Mock Description</dc:description>
     <dc:description>Mock Description</dc:description>
     <dc:date>2021-03-23</dc:date>
     <dc:date>2021-03-24</dc:date>
     <dc:type>text</dc:type>
     <dc:identifier>http://arxiv.org/abs/1004.3609</dc:identifier>
     <dc:identifier>Mock Identifier</dc:identifier>
     </oai_dc:dc>
    </metadata>
    </record>
    </OAI-PMH>
    """
    response = client.post("/records", json={"xml": xml_string})
    assert response.status_code == 201
    assert response.json == {"message": "Record added successfully"}

    get_response = client.get("/records")
    assert get_response.status_code == 200
    assert "oai:arXiv.org:1004.3608" in get_response.json["records"]


def test_get_article_with_valid_id(client):
    response = client.get("/article/oai:FakeArXiv.org:3456.7890")
    assert response.status_code == 200
    assert response.json == {
        "record": {
            "date": ["2022-01-04", "2022-01-05"],
            "identifier": "oai:FakeArXiv.org:3456.7890",
            "description": [
                " This is a fake description for debugging purposes. ",
                " This is a comment. ",
            ],
            "title": ["Fake Title"],
            "type": ["text"],
            "creators": ["Fake, Author B."],
            "subjects": ["Physic - Fake Subject"],
            "setspecs": ["physic"],
        }
    }


def test_get_article_with_invalid_id(client):
    response = client.get("/article/oai:FakeArXiv.org::invalid.invalid")
    assert response.status_code == 404
    assert response.json == {"error": "No record found with the given identifier"}


def test_get_summary_with_valid_id(client):
    response = client.get("/summary/oai:FakeArXiv.org:3456.7890")
    assert response.status_code == 200
    assert response.json == {
        "description": [
            " This is a fake description for debugging purposes. ",
            " This is a comment. ",
        ]
    }


def test_get_summary_with_invalid_id(client):
    response = client.get("/summary/oai:FakeArXiv.org::invalid.invalid")
    assert response.status_code == 404
    assert response.json == {"error": "No record found with the given identifier"}


def test_get_authors(client):
    response = client.get("/authors")
    assert response.status_code == 200
    assert "Fake, Author A." in response.json["authors"]
    assert "Fake, Author B." in response.json["authors"]
