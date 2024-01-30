# pylint: disable=redefined-outer-name
"""Testing the connection to the arXiv API."""
from xml.etree.ElementTree import Element
from src.connect_to_arxiv import ArXivHarvester, ArXivRecord
import requests_mock
from pytest import raises
from unittest.mock import patch
import re


def test_header_not_empty(record: ArXivRecord):
    header = record.header
    assert bool(header) is True


def test_header_contain_identifier(record: ArXivRecord):
    header = record.header
    if header is None:
        assert False
    assert isinstance(header["identifier"], str)


def test_header_contain_datestamp(record: ArXivRecord):
    header = record.header
    if header is None:
        assert False
    assert isinstance(header["datestamp"], str)


def test_header_contain_setspec(record: ArXivRecord):
    header = record.header
    if header is None:
        assert False
    assert isinstance(header["setSpec"], str)


def test_metadata_not_empty(record: ArXivRecord):
    metadata = record.metadata
    assert bool(metadata) is True


def test_metadata_contain_title(record: ArXivRecord):
    metadata = record.metadata
    if metadata is None:
        assert False
    assert isinstance(metadata["dc:title"], list)
    assert bool(metadata["dc:title"]) is True


def test_metadata_contain_creator(record: ArXivRecord):
    metadata = record.metadata
    if metadata is None:
        assert False
    assert isinstance(metadata["dc:creator"], list)
    assert bool(metadata["dc:creator"]) is True


def test_metadata_contain_subject(record: ArXivRecord):
    metadata = record.metadata
    if metadata is None:
        assert False
    assert isinstance(metadata["dc:subject"], list)
    assert bool(metadata["dc:subject"]) is True


def test_metadata_contain_description(record: ArXivRecord):
    metadata = record.metadata
    if metadata is None:
        assert False
    assert isinstance(metadata["dc:description"], list)
    assert bool(metadata["dc:description"]) is True


def test_metadata_contain_date(record: ArXivRecord):
    metadata = record.metadata
    if metadata is None:
        assert False
    assert isinstance(metadata["dc:date"], list)
    assert bool(metadata["dc:date"]) is True


def test_metadata_contain_identifier(record: ArXivRecord):
    metadata = record.metadata
    if metadata is None:
        assert False
    assert isinstance(metadata["dc:identifier"], list)
    assert bool(metadata["dc:identifier"]) is True


def test_metadata_contain_type(record: ArXivRecord):
    metadata = record.metadata
    if metadata is None:
        assert False
    assert isinstance(metadata["dc:type"], list)
    assert bool(metadata["dc:type"]) is True


def test_record_is_valid(record: ArXivRecord):
    assert isinstance(record, ArXivRecord)
    if (
        record.header is not None
        and record.metadata is not None
        and record.is_valid is True
    ):
        assert True
    else:
        assert False


def test_next_record_different(harvester: ArXivHarvester, record: ArXivRecord):
    header1 = record.header
    record = next(harvester.next_record())
    header2 = record.header
    assert header1 != header2


def test_record_same(record: ArXivRecord):
    header1 = record.header
    header2 = record.header
    assert header1 == header2


def test_two_harvest(harvester: ArXivHarvester, record: ArXivRecord):
    first_harvest_first_record = record.header
    for i, record in enumerate(
        harvester.next_record(), 0
    ):  # One harvest gives back 1000 elements, we are garanting a new harvest cycle by looping 999 time
        if i == 999:
            break
    first_harvest_last_record = record.header
    record = next(harvester.next_record())
    second_harvest_first_record = record.header

    # checking for empty dict
    assert bool(first_harvest_first_record) is True
    assert bool(first_harvest_last_record) is True
    assert bool(second_harvest_first_record) is True

    assert first_harvest_first_record != first_harvest_last_record
    assert first_harvest_first_record != second_harvest_first_record


def test_all_harvest(harvester: ArXivHarvester, record: ArXivRecord):
    first_record = record.header
    for record in harvester.next_record():
        pass
    last_record = record

    # checking for empty dict
    assert bool(first_record) is True
    assert bool(last_record) is True

    assert first_record != last_record


def test_correct_resumption_token_returned() -> None:
    with requests_mock.Mocker() as m, patch(
        "src.connect_to_arxiv.sleep", return_value=None
    ):
        m.get(re.compile("https://export.arxiv.org/oai2*"), status_code=503)

        with raises(ArXivHarvester.CustomHTTPException) as e:
            harvester = ArXivHarvester(
                from_date="2021-03-20",
                until_date="2021-03-30",
                set_cat="cs",
                resumption_token="6965856|1001",
            )
            next(harvester.next_record())

        assert e.value.resumption_token == "6965856|1001"


def test_resumption_token_with_harvester(requests_mock):
    with open("mock-response/request2.xml", "r", encoding="utf-8") as file:
        data2 = file.read()
    requests_mock.get(
        "https://export.arxiv.org/oai2?verb=ListRecords&resumptionToken=6965856|1001",
        text=data2,
    )

    harvester = ArXivHarvester(
        from_date="2021-03-20",
        until_date="2021-03-30",
        set_cat="cs",
        resumption_token="6965856|1001",
    )

    record = next(harvester.next_record())
    assert isinstance(record, ArXivRecord)
    if (
        record.header is not None
        and record.metadata is not None
        and record.is_valid is True
    ):
        assert True
    else:
        assert False
