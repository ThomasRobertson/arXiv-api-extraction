# pylint: disable=redefined-outer-name
"""Pytest config file"""
from neo4j import GraphDatabase
import pytest
from harvest_and_collect.connect_to_arxiv import ArXivHarvester, ArXivRecord
from harvest_and_collect.db_connexion import GraphDBConnexion
from neo4j.exceptions import ServiceUnavailable
from unittest.mock import Mock

# https://export.arxiv.org/oai2?verb=ListRecords&metadataPrefix=oai_dc&from=2021-03-20&until=2021-03-23&set=cs


@pytest.fixture(scope="function")
def harvester(requests_mock) -> ArXivHarvester:
    with open("mock-response/request1.xml", "r", encoding="utf-8") as file:
        data1 = file.read()
    requests_mock.get(
        "https://export.arxiv.org/oai2?verb=ListRecords&metadataPrefix=oai_dc&from=2021-03-20&until=2021-03-30&set=cs",
        text=data1,
    )

    with open("mock-response/request2.xml", "r", encoding="utf-8") as file:
        data2 = file.read()
    requests_mock.get(
        "https://export.arxiv.org/oai2?verb=ListRecords&resumptionToken=6965856|1001",
        text=data2,
    )

    with open("mock-response/request3.xml", "r", encoding="utf-8") as file:
        data3 = file.read()
    requests_mock.get(
        "https://export.arxiv.org/oai2?verb=ListRecords&resumptionToken=6965856|2001",
        text=data3,
    )

    harvester_return = ArXivHarvester(
        from_date="2021-03-20", until_date="2021-03-30", set_cat="cs"
    )
    return harvester_return


@pytest.fixture(scope="function")
def record(harvester) -> ArXivRecord:
    record_return = next(harvester.next_record())
    return record_return


@pytest.fixture(scope="session")
def db_connexion():
    try:  # try to access neo4://neo4j:7687, or default to localhost for local tests
        db_connexion_return: GraphDBConnexion = GraphDBConnexion("neo4j://neo4j:7687")
        db_connexion_return.driver.verify_connectivity()  # Call the method after instantiating the object
    except (ServiceUnavailable, ValueError):
        db_connexion_return = GraphDBConnexion("neo4j://localhost:7687")

    db_connexion_return.clean_database()  # clean database before launching tests
    return db_connexion_return


@pytest.fixture(scope="session")
def mock_record() -> ArXivRecord:
    record = Mock()
    record.header = {"identifier": "oai:FakeArXiv.org:3456.7890", "setSpec": "cs"}
    record.metadata = {
        "dc:title": ["Fake Title"],
        "dc:creator": ["Fake Author"],
        "dc:description": [" This is a fake description for debugging purposes. "],
        "dc:date": ["2022-01-04"],
        "dc:type": ["text"],
        "dc:subject": ["Computer and stuff"],
    }
    record.is_valid = True

    return record
