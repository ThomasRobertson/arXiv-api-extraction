import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from flask import Flask
from flask_restx import Api, Resource, reqparse
from harvest_and_collect.connect_to_arxiv import ArXivRecord
from harvest_and_collect.fill_data_base import GraphDBConnexion
from flask_restx import reqparse

db_connexion = GraphDBConnexion("neo4j://localhost:7687")


@api.route("/records")
class ListRecords(Resource):
    # Define the parser and add the 'limit' and 'category' arguments
    parser = reqparse.RequestParser()
    parser.add_argument("limit", type=int, help="Limit the number of records returned")
    parser.add_argument("category", type=str, help="Category of the records to return")

    def get(self):
        # Parse the arguments
        args = self.parser.parse_args()
        limit = args.get("limit")
        category = args.get("category")

        with db_connexion.driver.session() as session:
            # Modify the Cypher query to match records that have a connection to "Subject" nodes
            query = "MATCH (n:Record)-[:HAS_SUBJECT]->(s:Subject)"
            if category is not None:
                query += f" WHERE s.subject = '{category}'"
            query += " RETURN n.identifier AS identifier"
            if limit is not None:
                query += f" LIMIT {limit}"
            result = session.run(query)
            return {"records": [record["identifier"] for record in result]}


def create_app() -> Flask:
    app = Flask(__name__)
    api = Api(app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
