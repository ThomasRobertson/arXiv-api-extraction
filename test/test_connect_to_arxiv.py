"""Testing the connection to the arXiv API."""
import unittest

import connect_to_arxiv


class TestArXivResult(unittest.TestCase):
    def setUp(self):
        self.result = connect_to_arxiv.GetResponseFromAPI("physics.optics", 1, 10)

    def test_notempty(self):
        self.assertTrue(self.result)

    # def tearDown(self):


if __name__ == "__main__":
    unittest.main()
