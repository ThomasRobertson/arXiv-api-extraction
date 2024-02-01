"""
This module provides a Flask application for interacting with a Neo4j database that stores
ArXiv records.

The application provides several endpoints for querying the database:
- /authors: Returns a list of all authors in the database.
- /article/<id>: Returns the details of the article with the given identifier.
- /summary/<id>: Returns the summary of the article with the given identifier.
- /records: Returns a list of record identifiers. This endpoint accepts optional query
parameters for filtering the records.

The application also provides a POST endpoint at /records for adding a new record to the database.
The record must be provided as an XML string in the request body.

The application is configured to connect to a Neo4j database at the URI "neo4j://localhost:7687".
This can be changed by modifying the 'neo4j_driver' configuration variable.
"""

import argparse
from xml.etree import ElementTree as ET
from flask import Flask, request
from flask_restx import Api, Resource, reqparse, fields
from harvest_and_collect.connect_to_arxiv import ArXivRecord
from harvest_and_collect.db_connexion import GraphDBConnexion


parser = argparse.ArgumentParser(
    description="Launch the Flask app with a custom Neo4j URI."
)
# Add the '--neo4j_uri' argument
parser.add_argument("--neo4j_uri")
args = parser.parse_args()

app = Flask(__name__)
print(args.neo4j_uri)
app.config["neo4j_driver"] = GraphDBConnexion(args.neo4j_uri)
api = Api(app)


@api.route("/authors")
class ListAuthors(Resource):
    """List all of the authors present in the database."""

    @api.doc(description="List all of the authors present in the database.")
    def get(self):
        with app.config["neo4j_driver"].driver.session() as session:
            result = session.run("MATCH (a:Author) RETURN a.name AS name")
            return {"authors": [record["name"] for record in result]}


@api.route("/article/<string:id>")
@api.doc(
    params={"id": "Identifier of the article, ex: oai:arXiv.org:0912.0228"},
)
class GetArticle(Resource):
    """Get the details of an article."""

    @api.doc(description="Get the details of an article.")
    def get(self, id):
        with app.config["neo4j_driver"].driver.session() as session:
            result = session.run(
                """
                MATCH (r:Record {identifier: $id})
                OPTIONAL MATCH (r)-[:HAS_AUTHOR]->(a:Author)
                OPTIONAL MATCH (r)-[:HAS_SUBJECT]->(s:Subject)
                OPTIONAL MATCH (r)-[:HAS_SETSPEC]->(ss:SetSpec)
                RETURN r, collect(DISTINCT a.name) as creators, collect(DISTINCT s.subject) as subjects, collect(DISTINCT ss.setSpec) as setspecs
                """,
                id=id,
            )
            record = result.single()
            if record is None:
                return {"error": "No record found with the given identifier"}, 404
            # Convert the Neo4j Node object to a Python dictionary, otherwise we have a TypeError: not JSON serializable
            record_dict = dict(record["r"])
            record_dict["creators"] = record["creators"]
            record_dict["subjects"] = record["subjects"]
            record_dict["setspecs"] = record["setspecs"]
            return {"record": record_dict}


@api.route("/summary/<string:id>")
@api.doc(params={"id": "Identifier of the article, ex: oai:arXiv.org:0912.0228"})
class GetSummary(Resource):
    """Get the summary (descriptions) of an article.

    Note: there can be multiple description present in the article, such as other comments or notes.
    """

    @api.doc(
        description="Fetches the summary of the article with the given identifier."
    )
    def get(self, id):
        with app.config["neo4j_driver"].driver.session() as session:
            result = session.run(
                "MATCH (r:Record {identifier: $id}) RETURN r.description AS description",
                id=id,
            )
            record = result.single()
            if record is None:
                return {"error": "No record found with the given identifier"}, 404
            return {"description": record["description"]}


@api.route("/records")
class ListRecords(Resource):
    """
    In GET, list all of the records present.
    In POST, can add a new record in the XML format to the database.
    """

    # Define the parser and add the 'limit', 'category', 'author', and 'date' arguments
    parser = reqparse.RequestParser()
    parser.add_argument("limit", type=int, help="Limit the number of records returned")
    parser.add_argument("category", type=str, help="Category of the records to return")
    parser.add_argument("author", type=str, help="Author of the records to return")
    parser.add_argument("date", type=str, help="Date of the records to return")

    @api.expect(parser)
    @api.doc(
        description="Fetches a list of records from the database. The records can be filtered by limit, category, author, and date."
    )
    def get(self):
        # Parse the arguments
        route_args = self.parser.parse_args()
        limit = route_args.get("limit")
        category = route_args.get("category")
        author = route_args.get("author")
        date = route_args.get("date")

        # Check that limit is non-negative
        if limit is not None and limit < 0:
            return {"error": "Limit must be a non-negative integer"}, 400

        with app.config["neo4j_driver"].driver.session() as session:
            query = "MATCH (n:Record)"
            if date is not None:
                query += " WHERE ANY(d IN n.date WHERE d = $date)"
            if category is not None:
                query += (
                    " MATCH (n)-[:HAS_SUBJECT]->(s:Subject) WHERE s.subject = $category"
                )
            else:
                query += " OPTIONAL MATCH (n)-[:HAS_SUBJECT]->(s:Subject)"
            if author is not None:
                query += " MATCH (n)-[:HAS_AUTHOR]->(a:Author) WHERE a.name = $author"
            else:
                query += " OPTIONAL MATCH (n)-[:HAS_AUTHOR]->(a:Author)"
            query += " RETURN n.identifier AS identifier"
            if limit is not None:
                query += f" LIMIT {limit}"
            result = session.run(
                query, {"category": category, "author": author, "date": date}
            )
            return {"records": [record["identifier"] for record in result]}

    record_model = api.model(
        "Record",
        {
            "xml": fields.String(
                required=True, description="The XML string of the record to be added"
            )
        },
    )

    @api.expect(record_model)
    @api.doc(
        description="Adds a new record to the database. The record must be provided as an XML string in the OAI-PHM type in the request body.",
    )
    def post(self):
        if request.json is not None:
            xml_string = request.json.get("xml")
            if xml_string is not None:
                xml_element = ET.fromstring(xml_string)
                record = ArXivRecord(xml_element)
                if record.is_valid is True:
                    app.config["neo4j_driver"].add_record(record)
                    return {"message": "Record added successfully"}, 201
        return {"message": "Invalid request"}, 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
