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
        self.namespaces = {
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "oai_dc": "http://www.openarchives.org/OAI/2.0/oai_dc/",
            "oai": "http://www.openarchives.org/OAI/2.0/",
            "dc": "http://purl.org/dc/elements/1.1/",
        }
        self.record = self.records.next()

    def NextRecord(self) -> None:
        self.record = self.records.next()

    def GetRecordHeader(self) -> dict[str, str]:
        header = {}
        header["identifier"] = self.record.xml.find(
            "./oai:header/oai:identifier", self.namespaces
        ).text
        header["datestamp"] = self.record.xml.find(
            "./oai:header/oai:datestamp", self.namespaces
        ).text
        header["setSpec"] = self.record.xml.find(
            "./oai:header/oai:setSpec", self.namespaces
        ).text
        return header

    # def __GetListFromXlmElement(self):
