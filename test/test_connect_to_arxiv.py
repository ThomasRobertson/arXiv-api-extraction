"""Testing the connection to the arXiv API."""
import unittest
from src import connect_to_arxiv


class TestArXivResult(unittest.TestCase):
    def setUp(self):
        self.number_entries_requested = 10
        self.result = connect_to_arxiv.GetResponseFromAPI(
            1, self.number_entries_requested
        )

    def test_not_empty(self):
        self.assertTrue(self.result)

    def test_number_of_entries(self):
        number_of_headlines = len(self.result["entries"])
        self.assertEqual(number_of_headlines, self.number_entries_requested)

    # def tearDown(self):


if __name__ == "__main__":
    unittest.main()
