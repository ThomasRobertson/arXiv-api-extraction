# pylint: disable=redefined-outer-name
"""Testing the connection to the arXiv API."""
from xml.etree.ElementTree import Element
from src.connect_to_arxiv import ArXivHarvester, ArXivRecord


def test_header_not_empty(record: ArXivRecord):
    header = record.header
    assert bool(header) is True


def test_header_contain_identifier(record: ArXivRecord):
    header = record.header
    assert isinstance(header["identifier"], str)


def test_header_contain_datestamp(record: ArXivRecord):
    header = record.header
    assert isinstance(header["datestamp"], str)


def test_header_contain_setspec(record: ArXivRecord):
    header = record.header
    assert isinstance(header["setSpec"], str)


def test_metadata_not_empty(record: ArXivRecord):
    metadata = record.metadata
    assert bool(metadata) is True


def test_metadata_contain_title(record: ArXivRecord):
    metadata = record.metadata
    assert isinstance(metadata["dc:title"], list)
    assert bool(metadata["dc:title"]) is True


def test_metadata_contain_creator(record: ArXivRecord):
    metadata = record.metadata
    assert isinstance(metadata["dc:creator"], list)
    assert bool(metadata["dc:creator"]) is True


def test_metadata_contain_subject(record: ArXivRecord):
    metadata = record.metadata
    assert isinstance(metadata["dc:subject"], list)
    assert bool(metadata["dc:subject"]) is True


def test_metadata_contain_description(record: ArXivRecord):
    metadata = record.metadata
    assert isinstance(metadata["dc:description"], list)
    assert bool(metadata["dc:description"]) is True


def test_metadata_contain_date(record: ArXivRecord):
    metadata = record.metadata
    assert isinstance(metadata["dc:date"], list)
    assert bool(metadata["dc:date"]) is True


def test_metadata_contain_identifier(record: ArXivRecord):
    metadata = record.metadata
    assert isinstance(metadata["dc:identifier"], list)
    assert bool(metadata["dc:identifier"]) is True


def test_metadata_contain_type(record: ArXivRecord):
    metadata = record.metadata
    assert isinstance(metadata["dc:type"], list)
    assert bool(metadata["dc:type"]) is True


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
