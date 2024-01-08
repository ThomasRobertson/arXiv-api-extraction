# pylint: disable=redefined-outer-name
import pytest
from neo4j import GraphDatabase

URI = "neo4j://localhost:7687"

@pytest.fixture(scope="session")
def neo4j_driver():
    driver = GraphDatabase.driver(URI)
    yield driver
    driver.close()

def test_neo4j_connectivity(neo4j_driver):
    try: 
        neo4j_driver.verify_connectivity()
        assert True
    except Exception as e:
        pytest.fail(f"{e}")
