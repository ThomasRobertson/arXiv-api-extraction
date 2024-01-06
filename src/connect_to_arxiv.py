"""Connect to the arXiv API and return the results as entries of a FeedParserDict."""
from time import sleep
from requests import HTTPError
from sickle import Sickle


class BulkResponse:
    """Access in bulk meta-data from arXiv using OAI-PHM."""

    def __init__(self, from_date: str = "2012-12-12", until_date: str = "2012-12-19"):
        self.sickle = Sickle(
            "https://export.arxiv.org/oai2",
            retry_status_codes=[503],
            default_retry_after=5,
        )
        self.records = self.sickle.ListRecords(
            False,
            **{
                "metadataPrefix": "oai_dc",
                "from": {from_date},
                "until": {until_date},
            },
        )
        self.namespaces = {
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "oai_dc": "http://www.openarchives.org/OAI/2.0/oai_dc/",
            "oai": "http://www.openarchives.org/OAI/2.0/",
            "dc": "http://purl.org/dc/elements/1.1/",
        }
        self.NextRecord()

    def NextRecord(self) -> None:
        """Because Sickle is well implemented, the "retry_after" an HTTP error doesn't work.
        Here we are following arXiv API manual and waiting 5 seconds after a failed try.

        Raises:
            HTTPError: re-raising HTTP error
        """
        for i in range(3):
            try:
                self.record = self.records.next()
            except HTTPError as exc:
                if i == 2:
                    raise HTTPError from exc
                sleep(5)
                continue
            else:
                break

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

    def GetRecordMetadata(self) -> dict[str, str]:
        metadata = {}
        block_names = [
            "dc:title",
            "dc:creator",
            "dc:subject",
            "dc:description",
            "dc:date",
            "dc:type",
            "dc:identifier",
        ]
        for block_name in block_names:
            metadata[block_name] = self.__GetListFromXMLElement(block_name)
        return metadata

    def __GetListFromXMLElement(self, xml_block: str) -> list[str]:
        block = self.record.xml.findall(
            f"./oai:metadata/oai_dc:dc/{xml_block}", self.namespaces
        )
        block_list = [item.text for item in block]
        return block_list
