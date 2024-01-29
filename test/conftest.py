"""Pytest config file"""
import pytest
from src import connect_to_arxiv


@pytest.fixture(scope="session")
def harvester() -> connect_to_arxiv.ArXivHarvester:
    harvester_return = connect_to_arxiv.ArXivHarvesterOld()
    return harvester_return
