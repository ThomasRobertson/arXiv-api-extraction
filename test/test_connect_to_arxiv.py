# pylint: disable=redefined-outer-name
"""Testing the connection to the arXiv API."""
import pytest
from src import connect_to_arxiv

NUMBER_ENTRIES_REQUESTED = 10


@pytest.fixture
def setup_data():
    result = connect_to_arxiv.GetResponseFromAPI(1, NUMBER_ENTRIES_REQUESTED)
    yield result


def test_not_empty(setup_data):
    assert setup_data


def test_number_of_entries(setup_data):
    result = setup_data
    number_of_headlines = len(result["entries"])
    assert number_of_headlines == NUMBER_ENTRIES_REQUESTED
