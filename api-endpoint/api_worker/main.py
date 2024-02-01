import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import argparse
from flask import Flask, request
from flask_restx import Api, Resource, reqparse, fields
from harvest_and_collect.connect_to_arxiv import ArXivRecord
from harvest_and_collect.db_connexion import GraphDBConnexion
from xml.etree import ElementTree as ET


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["neo4j_driver"] = GraphDBConnexion("neo4j://localhost:7687")
    return app


app = create_app()
api = Api(app)


@api.route("/authors")
class ListAuthors(Resource):
    def get(self):
        with app.config["neo4j_driver"].driver.session() as session:
            result = session.run("MATCH (a:Author) RETURN a.name AS name")
            return {"authors": [record["name"] for record in result]}


@api.route("/article/<string:id>")
class GetArticle(Resource):
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
class GetSummary(Resource):
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
    # Define the parser and add the 'limit', 'category', 'author', and 'date' arguments
    parser = reqparse.RequestParser()
    parser.add_argument("limit", type=int, help="Limit the number of records returned")
    parser.add_argument("category", type=str, help="Category of the records to return")
    parser.add_argument("author", type=str, help="Author of the records to return")
    parser.add_argument("date", type=str, help="Date of the records to return")

    def get(self):
        # Parse the arguments
        args = self.parser.parse_args()
        limit = args.get("limit")
        category = args.get("category")
        author = args.get("author")
        date = args.get("date")

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

    @api.expect(api.model("Record", {"xml": fields.String(required=True)}))
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
    parser = argparse.ArgumentParser(
        description="Launch the Flask app with a custom Neo4j URI."
    )
    # Add the '--neo4j_uri' argument
    parser.add_argument("--neo4j_uri", action="store_true")
    args = parser.parse_args()
    app.run(debug=True)
