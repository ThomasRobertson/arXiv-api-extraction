"""Connect to the arXiv API and return the results as entries of a FeedParserDict."""
from time import sleep
from typing import Any, Generator
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET
import requests
from xml.etree import ElementTree


class ArXivHarvesterOld:
    """Access in bulk meta-data from arXiv using OAI-PHM."""

    # def __init__(self, from_date: str = "2012-12-12", until_date: str = "2012-12-19"):
    #     self.sickle = Sickle(
    #         "https://export.arxiv.org/oai2",
    #         retry_status_codes=[503],
    #         default_retry_after=5,
    #     )
    #     self.records = self.sickle.ListRecords(
    #         False,
    #         **{
    #             "metadataPrefix": "oai_dc",
    #             "from": from_date,
    #             "until": until_date,
    #         },
    #     )
    #     self.namespaces = {
    #         "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    #         "oai_dc": "http://www.openarchives.org/OAI/2.0/oai_dc/",
    #         "oai": "http://www.openarchives.org/OAI/2.0/",
    #         "dc": "http://purl.org/dc/elements/1.1/",
    #     }
    #     self.next_record()

    # def next_record(self) -> None:
    #     """Because Sickle is so well implemented, the "retry_after" an HTTP error doesn't work.
    #     Here we are following arXiv API manual and waiting 5 seconds after a failed try.

    #     Raises:
    #         HTTPError: re-raising HTTP error
    #     """
    #     for i in range(3):
    #         try:
    #             self.record = self.records.next()
    #         except requests.HTTPError as exc:
    #             if i == 2:
    #                 raise requests.HTTPError from exc
    #             sleep(5)
    #             continue
    #         else:
    #             break

    def __init__(self, from_date: str = "2012-12-12", until_date: str = "2012-12-19"):
        self.harvester = ArXivHarvester("2021-03-20", "2021-03-30", "cs")
        self.namespaces = {
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "oai_dc": "http://www.openarchives.org/OAI/2.0/oai_dc/",
            "oai": "http://www.openarchives.org/OAI/2.0/",
            "dc": "http://purl.org/dc/elements/1.1/",
        }
        self.record = next(self.harvester.next_record())

    def next_record(self):
        self.record = next(self.harvester.next_record())

    def get_record_header(self) -> dict[str, str]:
        header = {}
        header_fields = ["identifier", "datestamp", "setSpec"]
        for field in header_fields:
            header[field] = self.record.find(
                f"./oai:header/oai:{field}", self.namespaces
            ).text
        return header

    def get_record_metadata(self) -> dict[str, list[str]]:
        metadata = {}
        metadata_fields = [
            "dc:title",
            "dc:creator",
            "dc:subject",
            "dc:description",
            "dc:date",
            "dc:type",
            "dc:identifier",
        ]
        for field in metadata_fields:
            metadata[field] = self._get_list_from_xml_element(field)
        return metadata

    def _get_list_from_xml_element(self, xml_block: str) -> list[str]:
        block = self.record.findall(
            f"./oai:metadata/oai_dc:dc/{xml_block}", self.namespaces
        )
        block_list = [item.text for item in block]
        return block_list


class ArXivHarvester:
    """Acces the ArXiv database"""

    def __init__(self, from_date, until_date, set_cat) -> None:
        self.namespaces = {
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "oai_dc": "http://www.openarchives.org/OAI/2.0/oai_dc/",
            "oai": "http://www.openarchives.org/OAI/2.0/",
            "dc": "http://purl.org/dc/elements/1.1/",
        }
        self.resumption_token = None
        # https://export.arxiv.org/oai2?verb=ListRecords&metadataPrefix=oai_dc&from=2021-03-20&until=2021-03-23&set=cs
        self.from_date = from_date
        self.until_date = until_date
        self.set = set_cat
        self._get_new_records()

        self.records: list[Element]

    def _get_new_records(self) -> None:
        response = requests.Response
        for i in range(5):
            if self.resumption_token is None:
                response = requests.get(
                    f"https://export.arxiv.org/oai2?verb=ListRecords&metadataPrefix=oai_dc&from={self.from_date}&until={self.until_date}&set={self.set}"
                )
            else:
                response = requests.get(
                    f"https://export.arxiv.org/oai2?verb=ListRecords&resumptionToken={self.resumption_token}"
                )

            print(response.status_code)
            if response.status_code == 200:
                break
            elif response.status_code == 503:
                sleep(1 + i)  # incrementing the sleep time each time

        if response.status_code is not 200:
            print(f"Cannot connect to ArXiv, error code: {response.status_code}")
            raise requests.HTTPError

        try:
            xml_response = ET.fromstring(response.content)
            print(ET.tostring(xml_response, encoding="utf-8").decode()[:50])
        except ElementTree.ParseError as e:
            print(f"Failed to parse XML: {e}")
            raise Exception

        self._parse_records_response(xml_response)

    def _parse_records_response(self, response: Element) -> None:
        resumption_token_element = response.find(
            ".//oai:resumptionToken", self.namespaces
        )
        if resumption_token_element is not None:
            self.resumption_token = resumption_token_element.text
            self.cursor = resumption_token_element.get("cursor")
            self.complete_list_size = resumption_token_element.get("completeListSize")
        else:
            self.resumption_token = None
            self.cursor = None
            self.complete_list_size = None
        records = response.findall(".//oai:record", self.namespaces)
        self.records = [record for record in records]

    def next_record(self) -> Generator[Element, Any, None]:
        while True:
            if self.records:  # If there are records left
                yield self.records.pop(0)  # Return the next record
            else:  # If no records are left
                self._get_new_records()  # Fetch new records
                if (
                    not self.records
                ):  # If there are still no records after fetching, stop the generator
                    raise StopIteration
                yield self.records.pop(0)  # Return the first record of the new batch
