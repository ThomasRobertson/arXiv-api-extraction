"""Using the data from a harvester, add records to the database."""
from neo4j import GraphDatabase
from xml.etree.ElementTree import Element


class GraphDBConnexion:
    """Handle the database connection and provides functions to easily add records to it."""

    def __init__(self, uri: str) -> None:
        self.driver = GraphDatabase.driver(uri)

    def __del__(self) -> None:
        self.driver.close()

    def add_record(self, header: dict[str, str], metadata: dict[str, list[str]]):
        with self.driver.session(database="neo4j") as session:
            session.execute_write(self.record_tx, header, metadata)

    def record_tx(self, tx, header: dict[str, str], metadata: dict[str, list[str]]):
        # Create the Record node with properties from metadata
        record = tx.run(
            """
            MERGE (r:Record {identifier: $identifier, title: $title, description: $description, date: $date, type: $type})
            RETURN r.identifier AS record
            """,
            identifier=metadata["dc:identifier"],
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
        for creator in metadata["dc:creator"]:
            # Create the Author node with creator from metadata
            authorNode = tx.run(
                """
                MERGE (a:Author {creator: $creator})
                RETURN a.creator AS creator
                """,
                creator=creator,
            )

            # Create a relationship between the Record and Author nodes
            recordAuthorRelationship = tx.run(
                """
                MATCH (r:Record {identifier: $identifier}), (a:Author {creator: $creator})
                MERGE (r)-[rel:HAS_AUTHOR]->(a)
                RETURN type(rel) AS relationshipType
                """,
                identifier=metadata["dc:identifier"],
                creator=creator,
            )

        # Create a relationship between the Record and SetSpec nodes
        recordSetSpecRelationship = tx.run(
            """
            MATCH (r:Record {identifier: $identifier}), (s:SetSpec {setSpec: $setSpec})
            MERGE (r)-[rel:HAS_SETSPEC]->(s)
            RETURN type(rel) AS relationshipType
            """,
            identifier=metadata["dc:identifier"],
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
                identifier=metadata["dc:identifier"],
                subject=subject,
            )
