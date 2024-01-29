"""Tests for the Neo4j database"""
# pylint: disable=redefined-outer-name
import pytest
from neo4j import Driver, GraphDatabase
from src import fill_data_base
from src.connect_to_arxiv import ArXivHarvester

URI = "neo4j://localhost:7687"


@pytest.fixture(scope="session")
def neo4j_driver():
    driver = GraphDatabase.driver(URI)
    yield driver
    driver.close()


@pytest.fixture(scope="session")
def graph_db_connexion():
    connexion = fill_data_base.GraphDBConnexion
    return connexion


def test_neo4j_connectivity(neo4j_driver: Driver):
    try:
        neo4j_driver.verify_connectivity()
        assert True
    except Exception as e:
        pytest.fail(f"{e}")


def test_neo4j_add_header(
    graph_db_connexion: fill_data_base.GraphDBConnexion, harvester: ArXivHarvester
):
    connexion = graph_db_connexion()
    header = harvester.get_record_header()
    connexion.add_record_header(header)
    assert True


def test_neo4j_read_header(neo4j_driver: Driver, harvester: ArXivHarvester):
    header = harvester.get_record_header()
    driver = neo4j_driver
    with driver.session() as session:
        results = session.execute_read(read_header_tx, header)
    for result in results:  # Use the results outside the transaction
        value = result.value()
        assert (
            value["identifier"] == header["identifier"]
            and value["datestamp"] == header["datestamp"]
            and value["setSpec"] == header["setSpec"]
        ), "Result does not match header"


def read_header_tx(tx, header):
    result_cursor = tx.run(
        """
        MATCH (r:Record {identifier: $identifier})
        RETURN r
        """,
        identifier=header["identifier"],
    )
    results = [record for record in result_cursor]
    return results
