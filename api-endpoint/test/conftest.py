import pytest
import api_worker.main
from flask import Flask
from harvest_and_collect.fill_data_base import GraphDBConnexion
from neo4j.exceptions import ServiceUnavailable
from neo4j import Driver


@pytest.fixture()
def app() -> Flask:
    app = api_worker.main.app
    try:
        db_connexion: GraphDBConnexion = GraphDBConnexion("neo4j://neo4j:7687")
        db_connexion.driver.verify_connectivity()  # Call the method after instantiating the object
        app.config["neo4j_driver"] = GraphDBConnexion("neo4j://neo4j:7687")
    except (ServiceUnavailable, ValueError):
        app.config["neo4j_driver"] = GraphDBConnexion("neo4j://localhost:7687")
    # app.config["neo4j_driver"] = GraphDBConnexion("neo4j://neo4j:7687")
    app.config.update(
        {
            "TESTING": True,
        }
    )
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def db_connexion(app) -> GraphDBConnexion:
    db_connexion_return = app.config["neo4j_driver"]
    with db_connexion_return.driver.session() as session:
        session.run(
            "MATCH (n) DETACH DELETE n"
        )  # Clean the database before doing any test
        # Create some test data
        session.run(
            "CREATE (:Record {identifier: 'pytest_test1'})-[:HAS_SUBJECT]->(:Subject {subject: 'pytest_test'})"
        )
        session.run(
            "CREATE (:Record {identifier: 'pytest_test2'})-[:HAS_SUBJECT]->(:Subject {subject: 'pytest_test'})"
        )
    yield db_connexion_return

    with db_connexion_return.driver.session() as session:  # cleanup the database after doing any test.
        session.run("MATCH (n) DETACH DELETE n")  # Clean the database
