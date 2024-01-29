# pylint: disable=redefined-outer-name
"""Testing the connection to the arXiv API."""


def test_header_not_empty(harvester):
    header = harvester.get_record_header()
    assert bool(header) is True


def test_header_contain_identifier(harvester):
    header = harvester.get_record_header()
    assert isinstance(header["identifier"], str)


def test_header_contain_datestamp(harvester):
    header = harvester.get_record_header()
    assert isinstance(header["datestamp"], str)


def test_header_contain_setspec(harvester):
    header = harvester.get_record_header()
    assert isinstance(header["setSpec"], str)


def test_metadata_not_empty(harvester):
    metadata = harvester.get_record_metadata()
    assert bool(metadata) is True


def test_metadata_contain_title(harvester):
    metadata = harvester.get_record_metadata()
    assert isinstance(metadata["dc:title"], list)
    assert bool(metadata["dc:title"]) is True


def test_metadata_contain_creator(harvester):
    metadata = harvester.get_record_metadata()
    assert isinstance(metadata["dc:creator"], list)
    assert bool(metadata["dc:creator"]) is True


def test_metadata_contain_subject(harvester):
    metadata = harvester.get_record_metadata()
    assert isinstance(metadata["dc:subject"], list)
    assert bool(metadata["dc:subject"]) is True


def test_metadata_contain_description(harvester):
    metadata = harvester.get_record_metadata()
    assert isinstance(metadata["dc:description"], list)
    assert bool(metadata["dc:description"]) is True


def test_metadata_contain_date(harvester):
    metadata = harvester.get_record_metadata()
    assert isinstance(metadata["dc:date"], list)
    assert bool(metadata["dc:date"]) is True


def test_metadata_contain_identifier(harvester):
    metadata = harvester.get_record_metadata()
    assert isinstance(metadata["dc:identifier"], list)
    assert bool(metadata["dc:identifier"]) is True


def test_metadata_contain_type(harvester):
    metadata = harvester.get_record_metadata()
    assert isinstance(metadata["dc:type"], list)
    assert bool(metadata["dc:type"]) is True


def test_next_record_different(harvester):
    header1 = harvester.get_record_header()
    harvester.next_record()
    header2 = harvester.get_record_header()
    assert header1 != header2


def test_record_same(harvester):
    header1 = harvester.get_record_header()
    header2 = harvester.get_record_header()
    assert header1 == header2


def test_two_harvest(harvester):
    first_harvest_first_record = harvester.get_record_header()
    for _ in range(999):
        harvester.next_record()  # each request get 1000 records maximum, we are getting the last record.
    first_harvest_last_record = harvester.get_record_header()
    harvester.next_record()
    second_harvest_first_record = harvester.get_record_header()

    # checking for empty dict
    assert bool(first_harvest_first_record) is True
    assert bool(first_harvest_last_record) is True
    assert bool(second_harvest_first_record) is True

    assert first_harvest_first_record != first_harvest_last_record
    assert first_harvest_first_record != second_harvest_first_record
