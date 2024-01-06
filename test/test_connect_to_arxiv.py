# pylint: disable=redefined-outer-name
"""Testing the connection to the arXiv API."""
import pytest
from src import connect_to_arxiv


@pytest.fixture(scope="module")
def setup_data() -> connect_to_arxiv.BulkResponse:
    harvester = connect_to_arxiv.BulkResponse()
    return harvester


def test_header_not_empty(setup_data: connect_to_arxiv.BulkResponse):
    harvester = setup_data
    header = harvester.GetRecordHeader()
    assert header


def test_header_contain_identifier(setup_data: connect_to_arxiv.BulkResponse):
    harvester = setup_data
    header = harvester.GetRecordHeader()
    assert isinstance(header["identifier"], str)


def test_header_contain_datestamp(setup_data: connect_to_arxiv.BulkResponse):
    harvester = setup_data
    header = harvester.GetRecordHeader()
    assert isinstance(header["datestamp"], str)


def test_header_contain_setspec(setup_data: connect_to_arxiv.BulkResponse):
    harvester = setup_data
    header = harvester.GetRecordHeader()
    assert isinstance(header["setSpec"], str)


def test_next_record_different(setup_data: connect_to_arxiv.BulkResponse):
    harvester = setup_data
    header1 = harvester.GetRecordHeader()
    harvester.NextRecord()
    header2 = harvester.GetRecordHeader()
    assert header1 != header2


def test_record_same(setup_data: connect_to_arxiv.BulkResponse):
    harvester = setup_data
    header1 = harvester.GetRecordHeader()
    header2 = harvester.GetRecordHeader()
    assert header1 == header2


def test_two_harvest(setup_data: connect_to_arxiv.BulkResponse):
    harvester = setup_data
    first_harvest_first_record = harvester.GetRecordHeader()
    for _ in range(999):
        harvester.NextRecord()  # each request get 1000 records maximum, we are getting the last record.
    first_harvest_last_record = harvester.GetRecordHeader()
    harvester.NextRecord()
    second_harvest_first_record = harvester.GetRecordHeader()

    # checking for empty dict
    assert bool(first_harvest_first_record) is True
    assert bool(first_harvest_last_record) is True
    assert bool(second_harvest_first_record) is True

    assert first_harvest_first_record != first_harvest_last_record
    assert first_harvest_first_record != second_harvest_first_record
