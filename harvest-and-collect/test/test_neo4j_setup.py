"""Tests for the Neo4j database"""
# pylint: disable=redefined-outer-name
import pytest
from neo4j import Driver
from neo4j.exceptions import ServiceUnavailable

# from src import fill_data_base
# from src.connect_to_arxiv import ArXivHarvester
import signal


# class TimeoutException(Exception):
#     pass


# def timeout_handler(signum, frame):
#     raise TimeoutException


# # set the signal handler
# signal.signal(signal.SIGALRM, timeout_handler)


# def test_neo4j_connectivity(neo4j_driver: Driver):
#     try:
#         signal.alarm(5)  # Set an alarm for 5 seconds
#         neo4j_driver.verify_connectivity()
#         signal.alarm(0)  # Reset the alarm
#         assert True
#     except TimeoutException:
#         pytest.fail("Connection to Neo4j timed out.")
#     except ServiceUnavailable as e:
#         pytest.fail(f"{e}")
