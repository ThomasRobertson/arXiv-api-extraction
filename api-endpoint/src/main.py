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
    def get(self):
        with db_connexion.driver.session() as session:
            result = session.run("MATCH (n:Record) RETURN n.identifier AS identifier")
            return {"records": [record["identifier"] for record in result]}


if __name__ == "__main__":
    app.run(debug=True)
