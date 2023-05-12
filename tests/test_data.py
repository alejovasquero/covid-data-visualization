import unittest

from src.data import data_consumption


class DataTest(unittest.TestCase):

    def test_should_load_dataframe(self):
        df = data_consumption.obtain_file_as_dataframe(
            file="test.csv",
            directory=".",
            delimiter=";"
        )

        self.assertIsNotNone(df)
        self.assertEqual(2999, len(df))
