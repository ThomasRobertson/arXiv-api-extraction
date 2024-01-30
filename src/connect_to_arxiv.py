"""Connect to the arXiv API and return the results as entries of a FeedParserDict."""
from http.client import HTTPException
from time import sleep
from typing import Any, Generator
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET
import requests


class ArXivHarvester:
    """Acces the ArXiv database"""

    def __init__(self, **kwargs) -> None:
        self.from_date = kwargs.get("from_date")
        self.until_date = kwargs.get("until_date")
        self.set_cat = kwargs.get("set_cat")
        self.resumption_token = None
        self.namespaces = {
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "oai_dc": "http://www.openarchives.org/OAI/2.0/oai_dc/",
            "oai": "http://www.openarchives.org/OAI/2.0/",
            "dc": "http://purl.org/dc/elements/1.1/",
        }
        self.records = None

    def _get_new_records(self) -> None:
        # Exemple URL : https://export.arxiv.org/oai2?verb=ListRecords&metadataPrefix=oai_dc&from=2021-03-20&until=2021-03-23&set=cs
        response = requests.Response
        for i in range(5):
            if self.resumption_token is not None:
                response = requests.get(
                    f"https://export.arxiv.org/oai2?verb=ListRecords&resumptionToken={self.resumption_token}"
                )
                print(
                    f"INFO: Getting next request from ArXiv ({self.resumption_token})."
                )
            elif self.records is None:
                base_url = "https://export.arxiv.org/oai2?verb=ListRecords&metadataPrefix=oai_dc"
                if self.from_date is not None:
                    base_url += f"&from={self.from_date}"
                if self.until_date is not None:
                    base_url += f"&until={self.until_date}"
                if self.set_cat is not None:
                    base_url += f"&set={self.set_cat}"
                print("INFO: Getting first request from ArXiv.")
                response = requests.get(base_url)
            else:
                print("INFO: Got all of the records from ArXiv.")
                return

            # print(response.status_code)
            if response.status_code == 200:
                break
            elif response.status_code == 503:
                print(f"WARN: Error 503 received. Sleep {i + 1} seconds.")
                sleep(1 + i)  # incrementing the sleep time each time

        if response.status_code != 200:
            print(f"ERROR: Cannot connect to ArXiv, error code: {response.status_code}")
            raise HTTPException

        try:
            xml_response = ET.fromstring(response.content)  # type: ignore
            # print(ET.tostring(xml_response, encoding="utf-8").decode()[:50])
        except ET.ParseError as e:
            print(f"Failed to parse XML: {e}")
            raise ET.ParseError

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
                self.record = self.records[0]
                yield self.records.pop(0)  # Return the next record
            else:  # If no records are left
                self._get_new_records()  # Fetch new records
                if (
                    not self.records
                ):  # If there are still no records after fetching, stop the generator
                    return
                self.record = self.records[0]
                yield self.records.pop(0)  # Return the first record of the new batch

    def get_record_header(self, record: Element) -> dict[str, str]:
        header = {}
        header_fields = ["identifier", "datestamp", "setSpec"]
        for field in header_fields:
            record_field = record.find(f"./oai:header/oai:{field}", self.namespaces)
            if record_field is not None:
                header[field] = record_field.text
            else:
                header[field] = None
        return header

    def get_record_metadata(self, record: Element) -> dict[str, list[str]]:
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
            record_field = record.findall(
                f"./oai:metadata/oai_dc:dc/{field}", self.namespaces
            )
            if record_field:
                record_field = [item.text for item in record_field]
            else:
                record_field = None
            metadata[field] = record_field
        return metadata
