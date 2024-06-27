# import logging
import unittest
from os.path import abspath
from os.path import exists as file_exists
from shutil import copy2 as copy_file
from sys import path as environment_path

# add this project's local python path to the system path
code_path = abspath("./python")
environment_path.insert(1, code_path)
from categories_CSV_processor import CategoriesCSVProcessor

# add common python library's path to the system path
code_path = abspath("../local/python")
environment_path.insert(1, code_path)
from std_dbconn import get_database_connection
from std_logging import StdLogging

# add TRO's local python path to the system path
# code_path = abspath("../tro/local/python")
# environment_path.insert(1, code_path)


class CSVProcessorUnitTest(unittest.TestCase):
    _database_connection = None
    _test_file = None
    _csv_processor = None

    _logger = None

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self._logger = StdLogging(f"logs/{__name__}")

        self._database_connection = get_database_connection("devl")
        self._test_file = abspath("./stage/categories.csv")
        self._cvs_processor = CategoriesCSVProcessor(self._database_connection, self._test_file)

    # ---------------------------------------------------------------------------------------------------------------------
    def __del__(self):
        self._csv_processor = None
        self._test_file = None
        self._database_connection = None

        self._logger = None

    # ---------------------------------------------------------------------------------------------------------------------
    def setUp(self):
        # stage file with test category
        mock_file = abspath("./tests/mock_files/categories.csv")
        rc = copy_file(mock_file, self._test_file)
        return rc

    # ---------------------------------------------------------------------------------------------------------------------
    def test_1_file_found_then_renamed(self):
        input_file = self._test_file
        backup_file = "./stage/categories.csv.bkp"

        self.assertTrue(file_exists(input_file))
        self.assertFalse(file_exists(backup_file))

        self._cvs_processor.process_categories_file()

        self.assertFalse(file_exists(input_file))
        self.assertTrue(file_exists(backup_file))

    # ---------------------------------------------------------------------------------------------------------------------
    def test_2_rows_inserted(self):
        self._cvs_processor._categories_table.truncate()
        number_rows = self._cvs_processor._categories_table.get_row_count()
        self.assertEqual(number_rows, 0)

        self._cvs_processor.process_categories_file()

        number_rows = self._cvs_processor._categories_table.get_row_count()
        self.assertGreater(number_rows, 0)

    # ---------------------------------------------------------------------------------------------------------------------
    def tearDown(self):
        # self._test_table.truncate()
        # self._test_table = None
        # self._database_connection = None
        pass


if __name__ == "__main__":
    unittest.main()
