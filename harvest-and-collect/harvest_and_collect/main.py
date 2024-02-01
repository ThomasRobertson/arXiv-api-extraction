"""
This module provides the main entry point for the ArXiv harvesting application.

The main function in this module sets up a connection to the ArXiv database and the Neo4j
database, then fetches records from the ArXiv database and adds them to the Neo4j database.
It also handles command line arguments for running the application in mock mode, specifying
the Neo4j URI, and specifying the resumption token for the ArXiv database.
"""
import argparse
import requests_mock
from harvest_and_collect.connect_to_arxiv import ArXivHarvester
from harvest_and_collect.db_connexion import GraphDBConnexion


def main(
    mock=False,
    neo4j_uri="neo4j://localhost:7687",
    resumption_token=None,
    from_date="2021-03-20",
    until_date="2021-03-30",
    set_cat="cs",
):
    m = requests_mock.Mocker()
    if mock:
        m.start()
        with open("mock-response/request1.xml", "r", encoding="utf-8") as file:
            data1 = file.read()
        m.get(
            "https://export.arxiv.org/oai2?verb=ListRecords&metadataPrefix=oai_dc&from=2021-03-20&until=2021-03-30&set=cs",
            text=data1,
        )

        with open("mock-response/request2.xml", "r", encoding="utf-8") as file:
            data2 = file.read()
        m.get(
            "https://export.arxiv.org/oai2?verb=ListRecords&resumptionToken=6965856|1001",
            text=data2,
        )

        with open("mock-response/request3.xml", "r", encoding="utf-8") as file:
            data3 = file.read()
        m.get(
            "https://export.arxiv.org/oai2?verb=ListRecords&resumptionToken=6965856|2001",
            text=data3,
        )

    harvester = ArXivHarvester(
        from_date=from_date,
        until_date=until_date,
        set_cat=set_cat,
        resumption_token=resumption_token,
    )

    db_connexion = GraphDBConnexion(neo4j_uri)

    for record in harvester.next_record():
        db_connexion.add_record(record)

    if mock:
        m.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mock", action="store_true")
    parser.add_argument("--neo4j_uri", type=str)
    parser.add_argument("--resumption_token", type=str)
    parser.add_argument(
        "--from_date",
        type=str,
    )
    parser.add_argument(
        "--until_date",
        type=str,
    )
    parser.add_argument(
        "--set_cat",
        type=str,
    )
    args = parser.parse_args()
    try:
        main(
            mock=args.mock,
            neo4j_uri=args.neo4j_uri,
            resumption_token=args.resumption_token,
            from_date=args.from_date,
            until_date=args.until_date,
            set_cat=args.set_cat,
        )
    except ArXivHarvester.CustomHTTPException as e:
        error_message = f"ERROR: Request to ArVix timed out (Error {e.status_code})."
        error_message += f' Last resumption token is "{e.resumption_token}"'
        print("ERROR: Request to ArVix timed out.")
