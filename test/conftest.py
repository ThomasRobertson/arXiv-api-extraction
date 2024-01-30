# pylint: disable=redefined-outer-name
"""Pytest config file"""
from neo4j import GraphDatabase
import pytest
from src import connect_to_arxiv, fill_data_base

# https://export.arxiv.org/oai2?verb=ListRecords&metadataPrefix=oai_dc&from=2021-03-20&until=2021-03-23&set=cs


@pytest.fixture(scope="function")
def harvester(requests_mock) -> connect_to_arxiv.ArXivHarvester:
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

    harvester_return = connect_to_arxiv.ArXivHarvester(
        from_date="2021-03-20", until_date="2021-03-30", set_cat="cs"
    )
    return harvester_return


@pytest.fixture(scope="function")
def record(harvester):
    record_return = next(harvester.next_record())
    return record_return


@pytest.fixture(scope="session")
def neo4j_driver():
    driver = GraphDatabase.driver("neo4j://neo4j:7687")
    yield driver
    driver.close()


@pytest.fixture(scope="session")
def graph_db_connexion():
    connexion = fill_data_base.GraphDBConnexion
    return connexion
