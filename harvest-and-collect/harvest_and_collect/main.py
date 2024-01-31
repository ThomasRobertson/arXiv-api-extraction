import argparse
from http.client import HTTPException
import connect_to_arxiv
import fill_data_base
import requests_mock


def main(mock=False, neo4j_uri="neo4j://localhost:7687", resumption_token=None):
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

    harvester = connect_to_arxiv.ArXivHarvester(
        from_date="2021-03-20",
        until_date="2021-03-30",
        set_cat="cs",
        resumption_token=resumption_token,
    )

    db_connexion = fill_data_base.GraphDBConnexion("neo4j://localhost:7687")

    for i, record in enumerate(harvester.next_record()):
        # if i == 1:
        #     break
        db_connexion.add_record(record)

    if mock:
        m.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mock", action="store_true")
    parser.add_argument("--neo4j_uri", action="store_true")
    parser.add_argument("--resumption_token", action="store_true")
    args = parser.parse_args()
    try:
        main(
            mock=args.mock,
            neo4j_uri=args.neo4j_uri,
            resumption_token=args.resumption_token,
        )
    except connect_to_arxiv.ArXivHarvester.CustomHTTPException as e:
        error_message = f"ERROR: Request to ArVix timed out (Error {e.status_code})."
        error_message += f' Last resumption token is "{e.resumption_token}"'
        print(f"ERROR: Request to ArVix timed out.")
