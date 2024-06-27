# from os import path as Path
# import logging
import os

# from pathlib import Path
from shutil import copy2 as copy_file
from sys import path as search_path
from unittest import TestCase, main

code_path = os.path.abspath("../local/python")
search_path.insert(1, code_path)
from std_dbconn import get_database_connection
from std_logging import StdLogging, function_logger

code_path = os.path.abspath("../TRO/local/python")
search_path.insert(1, code_path)
from category_table import CategoriesTable

# code_path = os.path.abspath("./local/python")
# search_path.insert(1, code_path)
# from function_logger import function_logger


class TestLoadCategories(TestCase):
    _database_connection = None
    _test_table = None
    _test_category_name = None

    _logger = None

    # ---------------------------------------------------------------------------------------------------------------------
    def __init__(self, testName):
        super(TestLoadCategories, self).__init__(testName)
        self._logger = StdLogging(f"logs/{__name__}")

        self._database_connection = get_database_connection("devl")
        self._test_table = CategoriesTable(self._database_connection)
        self._test_category_name = "Test A:Test B:Test C"

    # ---------------------------------------------------------------------------------------------------------------------
    def __del__(self):
        self._test_category_name = None
        self._test_table = None
        self._database_connection = None

        self._logger = None

    # ---------------------------------------------------------------------------------------------------------------------
    def setUp(self):
        self._test_table.truncate()

    # ---------------------------------------------------------------------------------------------------------------------
    @function_logger
    def test_1_run_load(self):
        # category does not exist
        test_id = self._test_table.select_id_using_name(self._test_category_name)
        self.assertIsNone(test_id)

        # stage file with test category
        source_path = os.path.abspath("./tests/mock_files/categories_test_only.csv")
        destination_path = os.path.abspath("./stage/categories.csv")
        copy_file(source_path, destination_path)

        #  run the app
        os.system("python3 python/troload.py -e devl -t cat > logs/TROLoad.out 2> logs/TROLoad.err")

        # category now exist
        test_id = self._test_table.select_id_using_name(self._test_category_name)
        self.assertIsNotNone(test_id)

    # ---------------------------------------------------------------------------------------------------------------------
    def tearDown(self):
        pass


if __name__ == "__main__":
    main()
