"""Tests for the Neo4j database"""
# pylint: disable=redefined-outer-name


def test_add_record(db_connexion, record):
    db_connexion.add_record(record)

    # Check that the record was added to the database
    with db_connexion.driver.session(database="neo4j") as session:
        result = session.run(
            "MATCH (r:Record {identifier: $identifier}) RETURN r",
            identifier=record.header["identifier"],
        )
        assert result.single() is not None
    db_connexion.clean_database()


def test_add_invalid_record(db_connexion, record):
    record.is_valid = False  # Invalidated record

    db_connexion.add_record(record)

    # Check that the record was not added to the database
    with db_connexion.driver.session(database="neo4j") as session:
        result = session.run(
            "MATCH (r:Record {identifier: $identifier}) RETURN r",
            identifier=record.header["identifier"],
        )
        assert result.single() is None
    db_connexion.clean_database()


def test_clean_database(db_connexion, record):
    db_connexion.add_record(record)

    # Clean the database
    db_connexion.clean_database()

    # Check that the databse is empty
    with db_connexion.driver.session(database="neo4j") as session:
        result = session.run("MATCH (r:Record) RETURN r")
        assert result.peek() is None

    db_connexion.clean_database()
