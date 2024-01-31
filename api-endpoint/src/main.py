import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from flask import Flask
from flask_restx import Api, Resource, reqparse
from harvest_and_collect.connect_to_arxiv import ArXivRecord
from harvest_and_collect.fill_data_base import GraphDBConnexion
from flask_restx import reqparse

app = Flask(__name__)
api = Api(app)

db_connexion = GraphDBConnexion("neo4j://localhost:7687")


@api.route("/records")
class ListRecords(Resource):
    # Define the parser and add the 'limit' argument
    parser = reqparse.RequestParser()
    parser.add_argument("limit", type=int, help="Limit the number of records returned")

    def get(self):
        # Parse the arguments
        args = self.parser.parse_args()
        limit = args.get("limit")

        with db_connexion.driver.session() as session:
            # Add the LIMIT clause to the Cypher query if a limit is specified
            query = "MATCH (n:Record) RETURN n.identifier AS identifier"
            if limit is not None:
                query += f" LIMIT {limit}"
            result = session.run(query)
            return {"records": [record["identifier"] for record in result]}


if __name__ == "__main__":
    app.run(debug=True)
