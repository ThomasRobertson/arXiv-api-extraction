"""Using the data from a harvester, add records to the database."""
from neo4j import GraphDatabase
from harvest_and_collect.connect_to_arxiv import ArXivRecord


class GraphDBConnexion:
    """Handle the database connection and provides functions to easily add records to it."""

    def __init__(self, uri: str) -> None:
        self.driver = GraphDatabase.driver(uri)

    def __del__(self) -> None:
        self.driver.close()

    def add_record(self, record: ArXivRecord) -> None:
        if record.header is None or record.metadata is None or record.is_valid is False:
            print(f"ERROR: Record is not valid, canno't add it.")
            return
        with self.driver.session(database="neo4j") as session:
            session.execute_write(self._record_tx, record.header, record.metadata)

    def _record_tx(
        self, tx, header: dict[str, str], metadata: dict[str, list[str]]
    ) -> None:
        # Create the Record node with properties from metadata
        record = tx.run(
            """
            MERGE (r:Record {identifier: $identifier, title: $title, description: $description, date: $date, type: $type})
            RETURN r.identifier AS record
            """,
            identifier=header["identifier"],
            title=metadata["dc:title"],
            description=metadata["dc:description"],
            date=metadata["dc:date"],
            type=metadata["dc:type"],
        )

        # Create the SetSpec node with setSpec from the header
        setSpecNode = tx.run(
            """
            MERGE (s:SetSpec {setSpec: $setSpec})
            RETURN s.setSpec AS setSpec
            """,
            setSpec=header["setSpec"],
        )

        # Iterate over the creators in metadata and create an Author node for each
        for name in metadata["dc:creator"]:
            # Create the Author node with creator from metadata
            authorNode = tx.run(
                """
                MERGE (a:Author {name: $name})
                RETURN a.name AS name
                """,
                name=name,
            )

            # Create a relationship between the Record and Author nodes
            recordAuthorRelationship = tx.run(
                """
                MATCH (r:Record {identifier: $identifier}), (a:Author {name: $name})
                MERGE (r)-[rel:HAS_AUTHOR]->(a)
                RETURN type(rel) AS relationshipType
                """,
                identifier=header["identifier"],
                name=name,
            )

        # Create a relationship between the Record and SetSpec nodes
        recordSetSpecRelationship = tx.run(
            """
            MATCH (r:Record {identifier: $identifier}), (s:SetSpec {setSpec: $setSpec})
            MERGE (r)-[rel:HAS_SETSPEC]->(s)
            RETURN type(rel) AS relationshipType
            """,
            identifier=header["identifier"],
            setSpec=header["setSpec"],
        )

        # Iterate over the subjects in metadata and create a Subject node for each
        for subject in metadata["dc:subject"]:
            # Create the Subject node with subject from metadata
            subjectNode = tx.run(
                """
                MERGE (s:Subject {subject: $subject})
                RETURN s.subject AS subject
                """,
                subject=subject,
            )

            # Create a relationship between the Record and Subject nodes
            recordSubjectRelationship = tx.run(
                """
                MATCH (r:Record {identifier: $identifier}), (s:Subject {subject: $subject})
                MERGE (r)-[rel:HAS_SUBJECT]->(s)
                RETURN type(rel) AS relationshipType
                """,
                identifier=header["identifier"],
                subject=subject,
            )

    def clean_database(self) -> None:
        with self.driver.session(database="neo4j") as session:
            session.run("MATCH (n) DETACH DELETE n")
