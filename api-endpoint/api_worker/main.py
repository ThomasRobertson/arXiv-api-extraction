import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import argparse
from flask import Flask
from flask_restx import Api, Resource, reqparse
from harvest_and_collect.connect_to_arxiv import ArXivRecord
from harvest_and_collect.fill_data_base import GraphDBConnexion
from flask_restx import reqparse


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["neo4j_driver"] = GraphDBConnexion("neo4j://localhost:7687")
    return app


app = create_app()
api = Api(app)


@api.route("/hello")
class HelloWorld(Resource):
    def get(self):
        return {"hello": "world"}


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

        with app.config["neo4j_driver"].driver.session() as session:
            query = "MATCH (n:Record)"
            if date is not None:
                query += " WHERE n.date = $date"
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Launch the Flask app with a custom Neo4j URI."
    )
    # Add the '--neo4j_uri' argument
    parser.add_argument("--neo4j_uri", action="store_true")
    args = parser.parse_args()
    app.run(debug=True)
