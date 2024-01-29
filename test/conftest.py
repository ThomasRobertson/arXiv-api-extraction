"""Pytest config file"""
from neo4j import GraphDatabase
import pytest
from src import connect_to_arxiv, fill_data_base


# https://export.arxiv.org/oai2?verb=ListRecords&metadataPrefix=oai_dc&from=2021-03-20&until=2021-03-23&set=cs


@pytest.fixture(scope="session")
def harvester() -> connect_to_arxiv.ArXivHarvester:
    harvester_return = connect_to_arxiv.ArXivHarvester(
        from_date="2021-03-20", until_date="2021-03-30", set_cat="cs"
    )
    return harvester_return


@pytest.fixture(scope="session")
def record(harvester):
    record_return = next(harvester.next_record())
    return record_return


@pytest.fixture(scope="session")
def neo4j_driver():
    driver = GraphDatabase.driver("neo4j://localhost:7687")
    yield driver
    driver.close()


@pytest.fixture(scope="session")
def graph_db_connexion():
    connexion = fill_data_base.GraphDBConnexion
    return connexion
