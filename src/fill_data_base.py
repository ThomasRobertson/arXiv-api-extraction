"""Using the data from a harvester, add records to the database."""
from neo4j import GraphDatabase
from xml.etree.ElementTree import Element


class GraphDBConnexion:
    """Handle the database connection and provides functions to easily add records to it."""

    def __init__(self) -> None:
        self.driver = GraphDatabase.driver("neo4j://localhost:7687")

    def __del__(self) -> None:
        self.driver.close()

    def add_record_header(self, header: dict[str, str]) -> None:
        with self.driver.session(database="neo4j") as session:
            session.execute_write(self.record_header_tx, header)

    def record_header_tx(self, tx, header: dict[str, str]):
        record = tx.run(
            """
            MERGE (r:Record {identifier: $identifier, datestamp:$datestamp, setSpec:$setSpec})
            RETURN r.identifier AS record
            """,
            identifier=header["identifier"],
            datestamp=header["datestamp"],
            setSpec=header["setSpec"],
        )

    def add_record(self, header: dict[str, str], metadata: dict[str, list[str]]):
        with self.driver.session(database="neo4j") as session:
            session.execute_write(self.record_tx, header, metadata)

    def record_tx(self, tx, header: dict[str, str], metadata: dict[str, list[str]]):
        # Create the first node with properties from metadata
        record = tx.run(
            """
            MERGE (r:Record {identifier: $identifier, title: $title, description: $description, date: $date, type: $type})
            RETURN r.identifier AS record
            """,
            identifier=metadata["identifier"],
            title=metadata["title"],
            description=metadata["description"],
            date=metadata["date"],
            type=metadata["type"],
        )

        # Create the second node with setSpec from the header
        setSpecNode = tx.run(
            """
            MERGE (s:SetSpec {setSpec: $setSpec})
            RETURN s.setSpec AS setSpec
            """,
            setSpec=header["setSpec"],
        )

        # Create a relationship between the two nodes
        relationship = tx.run(
            """
            MATCH (r:Record {identifier: $identifier}), (s:SetSpec {setSpec: $setSpec})
            MERGE (r)-[rel:HAS_SETSPEC]->(s)
            RETURN type(rel) AS relationshipType
            """,
            identifier=metadata["identifier"],
            setSpec=header["setSpec"],
        )
