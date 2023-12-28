import unittest

from src.connectToArXiv import getResponseFromAPI


class TestArXivResult(unittest.TestCase):
    def setUp(self):
        self.result = getResponseFromAPI("physics.optics", 1, 10)

    def test_notempty(self):
        self.assertTrue(self.result)

    # def tearDown(self):


if __name__ == "__main__":
    unittest.main()
