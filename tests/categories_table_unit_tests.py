# import logging
import unittest
from os.path import abspath as full_path
from sys import path as environment_path

# add this project's local python path to the system path
# code_path = full_path("./local/python")
# environment_path.insert(1, code_path)

# add my common python library's path to the system path
code_path = full_path("../local/python")
environment_path.insert(1, code_path)
# from function_logger import function_logger
from std_dbconn import get_database_connection
from std_logging import StdLogging, function_logger

# add TRO's local python path to the system path
code_path = full_path("../tro/local/python")
environment_path.insert(1, code_path)
from category_data import CategoryData
from category_table import CategoriesTable


class CategoriesTableUnitTests(unittest.TestCase):
    _database_connection = None
    _test_table = None

    _logger = None

    # ---------------------------------------------------------------------------------------------------------------------
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self._logger = StdLogging(f"logs/{__name__}")

        self._database_connection = get_database_connection("devl")
        self._test_table = CategoriesTable(self._database_connection)

    # ---------------------------------------------------------------------------------------------------------------------
    @function_logger
    def setUp(self):
        self._test_table.truncate()

    # ---------------------------------------------------------------------------------------------------------------------
    @function_logger
    def test_1_select(self):
        category_name = "TestCat_1"
        missing_id = self._test_table.select_id_using_name(category_name)
        self.assertIsNone(missing_id)

    # ---------------------------------------------------------------------------------------------------------------------
    @function_logger
    def test_2_insert(self):
        category_name = "TestCat_2"
        category_data = CategoryData(category_name)
        missing_id = self._test_table.select_id_using_name(category_name)
        self.assertIsNone(missing_id)
        inserted_id = self._test_table.insert(category_data)
        self.assertIsNotNone(inserted_id)
        selected_id = self._test_table.select_id_using_name(category_name)
        self.assertEqual(inserted_id, selected_id)

    # ---------------------------------------------------------------------------------------------------------------------
    @function_logger
    def test_3_update(self):
        initial_name = "TestCat_3"
        initial_data = CategoryData(initial_name)
        new_name = "TestCat_3_updated"
        new_data = CategoryData(new_name)

        selected_id = self._test_table.select_id_using_name(initial_name)
        self.assertIsNone(selected_id)

        inserted_id = self._test_table.insert(initial_data)
        self.assertIsNotNone(inserted_id)

        # self._logger.debug(f"Well ? inserted_id = {inserted_id}")
        # self._logger.debug(f"Well ? new_data = {new_data}")
        self._test_table.update(inserted_id, new_data)

        selected_id = self._test_table.select_id_using_name(initial_name)
        self.assertIsNone(selected_id)
        inserted_id = self._test_table.select_id_using_name(new_name)
        self.assertIsNotNone(inserted_id)

    # ---------------------------------------------------------------------------------------------------------------------
    @function_logger
    def test_4_delete(self):
        category_name = "TestCat_4"

        selected_id = self._test_table.select_id_using_name(category_name)
        self.assertIsNone(selected_id)

        test_category = CategoryData(category_name)
        inserted_id = self._test_table.insert(test_category)
        self.assertIsNotNone(inserted_id)

        rows_deleted = self._test_table.delete_by_id(inserted_id)
        self.assertEqual(rows_deleted, 1)

        selected_id = self._test_table.select_id_using_name(category_name)
        self.assertIsNone(selected_id)

    # ---------------------------------------------------------------------------------------------------------------------
    @function_logger
    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
