"""Using the data from a harvester, add records to the database."""
from neo4j import GraphDatabase


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
