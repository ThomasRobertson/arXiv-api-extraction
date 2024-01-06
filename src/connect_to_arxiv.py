"""Connect to the arXiv API and return the results as entries of a FeedParserDict."""
from sickle import Sickle


class BulkResponse:
    """Access in bulk meta-data from arXiv using OAI-PHM."""

    def __init__(self, from_date: str = "2012-12-12", until_date: str = "2012-12-19"):
        self.sickle = Sickle("https://export.arxiv.org/oai2")
        self.records = self.sickle.ListRecords(
            False,
            **{
                "metadataPrefix": "oai_dc",
                "from": {from_date},
                "until": {until_date},
            }
        )
        self.records = self.records.next()
        self.namespaces = {
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "oai_dc": "http://www.openarchives.org/OAI/2.0/oai_dc/",
            "oai": "http://www.openarchives.org/OAI/2.0/",
            "dc": "http://purl.org/dc/elements/1.1/",
        }

    def GetNextRecord(self) -> None:
        self.records = self.records.next()
