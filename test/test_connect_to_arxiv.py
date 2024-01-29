# pylint: disable=redefined-outer-name
"""Testing the connection to the arXiv API."""
from xml.etree.ElementTree import Element
from src.connect_to_arxiv import ArXivHarvester


def test_header_not_empty(harvester: ArXivHarvester, record: Element):
    header = harvester.get_record_header(record)
    assert bool(header) is True


def test_header_contain_identifier(harvester: ArXivHarvester, record: Element):
    header = harvester.get_record_header(record)
    assert isinstance(header["identifier"], str)


def test_header_contain_datestamp(harvester: ArXivHarvester, record: Element):
    header = harvester.get_record_header(record)
    assert isinstance(header["datestamp"], str)


def test_header_contain_setspec(harvester: ArXivHarvester, record: Element):
    header = harvester.get_record_header(record)
    assert isinstance(header["setSpec"], str)


def test_metadata_not_empty(harvester: ArXivHarvester, record: Element):
    metadata = harvester.get_record_metadata(record)
    assert bool(metadata) is True


def test_metadata_contain_title(harvester: ArXivHarvester, record: Element):
    metadata = harvester.get_record_metadata(record)
    assert isinstance(metadata["dc:title"], list)
    assert bool(metadata["dc:title"]) is True


def test_metadata_contain_creator(harvester: ArXivHarvester, record: Element):
    metadata = harvester.get_record_metadata(record)
    assert isinstance(metadata["dc:creator"], list)
    assert bool(metadata["dc:creator"]) is True


def test_metadata_contain_subject(harvester: ArXivHarvester, record: Element):
    metadata = harvester.get_record_metadata(record)
    assert isinstance(metadata["dc:subject"], list)
    assert bool(metadata["dc:subject"]) is True


def test_metadata_contain_description(harvester: ArXivHarvester, record: Element):
    metadata = harvester.get_record_metadata(record)
    assert isinstance(metadata["dc:description"], list)
    assert bool(metadata["dc:description"]) is True


def test_metadata_contain_date(harvester: ArXivHarvester, record: Element):
    metadata = harvester.get_record_metadata(record)
    assert isinstance(metadata["dc:date"], list)
    assert bool(metadata["dc:date"]) is True


def test_metadata_contain_identifier(harvester: ArXivHarvester, record: Element):
    metadata = harvester.get_record_metadata(record)
    assert isinstance(metadata["dc:identifier"], list)
    assert bool(metadata["dc:identifier"]) is True


def test_metadata_contain_type(harvester: ArXivHarvester, record: Element):
    metadata = harvester.get_record_metadata(record)
    assert isinstance(metadata["dc:type"], list)
    assert bool(metadata["dc:type"]) is True


def test_next_record_different(harvester: ArXivHarvester, record: Element):
    header1 = harvester.get_record_header(record)
    record = next(harvester.next_record())
    header2 = harvester.get_record_header(record)
    assert header1 != header2


def test_record_same(harvester: ArXivHarvester, record: Element):
    header1 = harvester.get_record_header(record)
    header2 = harvester.get_record_header(record)
    assert header1 == header2


def test_two_harvest(harvester: ArXivHarvester, record: Element):
    first_harvest_first_record = harvester.get_record_header(record)
    for i, record in enumerate(
        harvester.next_record(), 0
    ):  # One harvest gives back 1000 elements, we are garanting a new harvest cycle by looping 999 time
        if i == 999:
            break
    first_harvest_last_record = harvester.get_record_header(record)
    record = next(harvester.next_record())
    second_harvest_first_record = harvester.get_record_header(record)

    # checking for empty dict
    assert bool(first_harvest_first_record) is True
    assert bool(first_harvest_last_record) is True
    assert bool(second_harvest_first_record) is True

    assert first_harvest_first_record != first_harvest_last_record
    assert first_harvest_first_record != second_harvest_first_record
