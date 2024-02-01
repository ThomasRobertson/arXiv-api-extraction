import pytest
import api_worker.main
from flask import Flask
from harvest_and_collect.fill_data_base import GraphDBConnexion
from harvest_and_collect.connect_to_arxiv import ArXivRecord
from neo4j.exceptions import ServiceUnavailable
from neo4j import Driver
from xml.etree import ElementTree as ET


@pytest.fixture()
def app() -> Flask:
    app = api_worker.main.app
    try:
        db_connexion: GraphDBConnexion = GraphDBConnexion("neo4j://neo4j:7687")
        db_connexion.driver.verify_connectivity()  # Call the method after instantiating the object
        app.config["neo4j_driver"] = GraphDBConnexion("neo4j://neo4j:7687")
    except (ServiceUnavailable, ValueError):
        app.config["neo4j_driver"] = GraphDBConnexion("neo4j://localhost:7687")
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
def db_connexion(app) -> GraphDBConnexion:  # type: ignore
    db_connexion_return = app.config["neo4j_driver"]
    db_connexion_return.clean_database()

    xml_post = {
        """<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
        <record>
        <header>
         <identifier>oai:FakeArXiv.org:1234.5678</identifier>
         <datestamp>2022-01-01</datestamp>
         <setSpec>cs</setSpec>
        </header>
        <metadata>
         <oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
         <dc:title>Fake Title</dc:title>
         <dc:creator>Fake, Author A.</dc:creator>
         <dc:subject>Computer Science - Fake Subject</dc:subject>
         <dc:description> This is a fake description for debugging purposes. </dc:description>
         <dc:description> This is a comment. </dc:description>
         <dc:date>2022-01-02</dc:date>
         <dc:date>2022-01-03</dc:date>
         <dc:type>text</dc:type>
         <dc:identifier>http://fakearxiv.org/abs/1234.5678</dc:identifier>
         </oai_dc:dc>
        </metadata>
        </record>
        </OAI-PMH>""",
        """
        <OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
        <record>
        <header>
         <identifier>oai:FakeArXiv.org:2345.6789</identifier>
         <datestamp>2022-01-01</datestamp>
         <setSpec>cs</setSpec>
        </header>
        <metadata>
         <oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
         <dc:title>Fake Title</dc:title>
         <dc:creator>Fake, Author B.</dc:creator>
         <dc:subject>Computer Science - Fake Subject</dc:subject>
         <dc:description> This is a fake description for debugging purposes. </dc:description>
         <dc:description> This is a comment. </dc:description>
         <dc:date>2022-01-02</dc:date>
         <dc:date>2022-01-03</dc:date>
         <dc:type>text</dc:type>
         <dc:identifier>http://fakearxiv.org/abs/2345.6789</dc:identifier>
         </oai_dc:dc>
        </metadata>
        </record>
        </OAI-PMH>""",
        """<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
        <record>
        <header>
         <identifier>oai:FakeArXiv.org:3456.7890</identifier>
         <datestamp>2022-01-02</datestamp>
         <setSpec>physic</setSpec>
        </header>
        <metadata>
         <oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
         <dc:title>Fake Title</dc:title>
         <dc:creator>Fake, Author B.</dc:creator>
         <dc:subject>Physic - Fake Subject</dc:subject>
         <dc:description> This is a fake description for debugging purposes. </dc:description>
         <dc:description> This is a comment. </dc:description>
         <dc:date>2022-01-04</dc:date>
         <dc:date>2022-01-05</dc:date>
         <dc:type>text</dc:type>
         <dc:identifier>http://fakearxiv.org/abs/3456.7890</dc:identifier>
         </oai_dc:dc>
        </metadata>
        </record>
        </OAI-PMH>""",
    }

    for xml in xml_post:
        xml_element = ET.fromstring(xml)
        record = ArXivRecord(xml_element)
        if record.is_valid is True:
            app.config["neo4j_driver"].add_record(record)
        else:
            assert False
    yield db_connexion_return  # type: ignore

    # with db_connexion_return.driver.session() as session:  # cleanup the database after doing any test.
    #     session.run("MATCH (n) DETACH DELETE n")  # Clean the database
