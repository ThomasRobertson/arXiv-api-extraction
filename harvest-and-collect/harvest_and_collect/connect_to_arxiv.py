"""
This module provides classes to connect to and harvest records from the ArXiv database.

Classes:
    ArXivRecord: Represents a single record from the ArXiv database.
    ArXivHarvester: Handles the connection to the ArXiv database and fetches records.

The ArXivRecord class parses XML data from a single ArXiv record into a Python object.
It extracts the header and metadata from the record and checks if the record is valid.

The ArXivHarvester class connects to the ArXiv database and fetches records.
It handles HTTP exceptions and retries failed requests.
It also handles pagination by using the resumption token provided by the ArXiv API.
"""
from http.client import HTTPException
from time import sleep
from typing import Any, Generator
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET
import requests


class ArXivRecord:
    """A class to represent a single record from the ArXiv database."""

    def __init__(self, record_xml: Element) -> None:
        self._namespaces = {
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "oai_dc": "http://www.openarchives.org/OAI/2.0/oai_dc/",
            "oai": "http://www.openarchives.org/OAI/2.0/",
            "dc": "http://purl.org/dc/elements/1.1/",
        }
        self._record_xml: Element = record_xml
        self.header = self._get_record_header()
        self.metadata = self._get_record_metadata()
        if (
            self.header is None or self.metadata is None
        ):  # If header or metadata is not valid, set everything to None
            self.header = None
            self.metadata = None
            self.is_valid: bool = False
        else:
            self.is_valid: bool = True

    def _get_record_header(self) -> dict[str, str] | None:
        header = {}
        header_fields = ["identifier", "setSpec"]
        for field in header_fields:
            record_field = self._record_xml.find(
                f".//oai:header/oai:{field}", self._namespaces
            )
            if record_field is not None:
                header[field] = record_field.text
            else:
                return None
        return header

    def _get_record_metadata(self) -> dict[str, list[str]] | None:
        metadata = {}
        metadata_fields = [
            "dc:title",
            "dc:creator",
            "dc:subject",
            "dc:description",
            "dc:date",
            "dc:type",
            # "dc:identifier",
        ]
        for field in metadata_fields:
            record_field = self._record_xml.findall(
                f".//oai:metadata/oai_dc:dc/{field}", self._namespaces
            )
            if record_field:
                record_field = [item.text for item in record_field]
            else:
                return None
            metadata[field] = record_field
        return metadata


class ArXivHarvester:
    """A class to handle the connection to the ArXiv database and fetch records.

    Raises:
        ArXivHarvester.CustomHTTPException: Custom HTTP Exception that forward the status code and the resumption token, if any.

    Yields:
        next_record(): Yields the next record from the fetched records.
    """

    class CustomHTTPException(HTTPException):
        """Custom HTTP Exception that forward the status code and the resumption token, if any."""

        def __init__(self, status_code, resumption_token) -> None:
            super().__init__()
            self.status_code = status_code
            self.resumption_token = resumption_token

    def __init__(self, **kwargs) -> None:
        if "from_date" in kwargs and kwargs.get("from_date") is not False:
            self._from_date = kwargs.get("from_date")
        else:
            self._from_date = None

        if "until_date" in kwargs and kwargs.get("until_date") is not False:
            self._until_date = kwargs.get("until_date")
        else:
            self._until_date = None

        if "set_cat" in kwargs and kwargs.get("set_cat") is not False:
            self._set_cat = kwargs.get("set_cat")
        else:
            self._set_cat = None

        if "resumption_token" in kwargs and kwargs.get("resumption_token") is not False:
            self._resumption_token = kwargs.get("resumption_token")
        else:
            self._resumption_token = None

        self._namespaces = {
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "oai_dc": "http://www.openarchives.org/OAI/2.0/oai_dc/",
            "oai": "http://www.openarchives.org/OAI/2.0/",
            "dc": "http://purl.org/dc/elements/1.1/",
        }
        self._records = None
        self.cursor = None
        self.complete_list_size = None
        self.record = None

    def _get_new_records(self) -> None:
        response = requests.Response
        for i in range(5):
            if self._resumption_token is not None:
                response = requests.get(
                    f"https://export.arxiv.org/oai2?verb=ListRecords&resumptionToken={self._resumption_token}",
                    timeout=5,
                )

                print(
                    f"INFO: Getting next request from ArXiv ({self._resumption_token})."
                )
            elif self._records is None:
                base_url = "https://export.arxiv.org/oai2?verb=ListRecords&metadataPrefix=oai_dc"
                if self._from_date is not None:
                    base_url += f"&from={self._from_date}"
                if self._until_date is not None:
                    base_url += f"&until={self._until_date}"
                if self._set_cat is not None:
                    base_url += f"&set={self._set_cat}"
                print("INFO: Getting first request from ArXiv.")
                response = requests.get(base_url, timeout=5)
            else:
                print("INFO: Got all of the records from ArXiv.")
                return

            # print(response.status_code)
            if response.status_code == 200:
                break
            if response.status_code == 503:
                print(f"WARN: Error 503 received. Sleep {i + 1} seconds.")
                sleep(1 + i)  # incrementing the sleep time each time

        if response.status_code != 200:
            print(f"ERROR: Cannot connect to ArXiv, error code: {response.status_code}")
            raise ArXivHarvester.CustomHTTPException(
                response.status_code, self._resumption_token
            )

        try:
            xml_response = ET.fromstring(response.content)  # type: ignore
            # print(ET.tostring(xml_response, encoding="utf-8").decode()[:50])
        except ET.ParseError as e:
            print(f"Failed to parse XML: {e}")
            raise ET.ParseError

        self._parse_records_response(xml_response)

    def _parse_records_response(self, response: Element) -> None:
        resumption_token_element = response.find(
            ".//oai:resumptionToken", self._namespaces
        )
        if resumption_token_element is not None:
            self._resumption_token = resumption_token_element.text
            self.cursor = resumption_token_element.get("cursor")
            self.complete_list_size = resumption_token_element.get("completeListSize")
        else:
            self._resumption_token = None
            self.cursor = None
            self.complete_list_size = None
        records = response.findall(".//oai:record", self._namespaces)
        self._records = list(records)

    def next_record(self) -> Generator[ArXivRecord, Any, None]:
        """
        A generator method that yields the next record from the fetched records.

        This method continuously yields records from the fetched records list. If the list is empty, it fetches a new batch
        of records from the ArXiv database. If there are still no records after fetching, it stops the generator.

        Yields:
        ArXivRecord : The next record from the fetched records.

        Raises:
        CustomHTTPException : If an HTTP error occurs while fetching new records.
        """
        while True:
            if self._records:  # If there are records left
                self.record = self._records[0]
                record = ArXivRecord(self._records.pop(0))
                yield record  # Return the next record
            else:  # If no records are left
                self._get_new_records()  # Fetch new records
                if (
                    not self._records
                ):  # If there are still no records after fetching, stop the generator
                    return
                self.record = self._records[0]
                record = ArXivRecord(self._records.pop(0))
                yield record  # Return the first record of the new batch
