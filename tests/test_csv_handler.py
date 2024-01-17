import unittest
from evaluation.utility.csv_handler import read_csv
import csv
import os


class TestCSVHandler(unittest.TestCase):
    def setUp(self):
        # Create a temporary CSV file for testing
        self.test_csv_path = "data/test_input.csv"
        with open(self.test_csv_path, "w", newline="") as test_file:
            writer = csv.writer(test_file)
            writer.writerows(
                [
                    ["Name", "Age", "City"],
                    ["John Doe", "25", "New York"],
                    ["Jane Smith", "30", "San Francisco"],
                ]
            )

    def tearDown(self):
        # Remove the temporary CSV file after testing
        os.remove(self.test_csv_path)

    def test_read_csv(self):
        # Test if the CSV is read correctly
        expected_data = [
            ["Name", "Age", "City"],
            ["John Doe", "25", "New York"],
            ["Jane Smith", "30", "San Francisco"],
        ]
        actual_data = read_csv(self.test_csv_path)
        self.assertEqual(actual_data, expected_data)


if __name__ == "__main__":
    unittest.main()
