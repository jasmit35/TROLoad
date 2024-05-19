import os
import sys
import unittest

code_path = os.path.abspath("./local/python")
sys.path.insert(1, code_path)
from function_wrapper import function_wrapper

tro_code_path = os.path.abspath("../tro/local/python")
sys.path.insert(1, tro_code_path)
from categories import CategoriesTable

tro_code_path = os.path.abspath("../local/python")
sys.path.insert(1, tro_code_path)
from std_dbconn import get_database_connection


class TestCategories(unittest.TestCase):
    #     _database_connection = None
    #     _test_table = None

    def setUp(self):
        self._database_connection = get_database_connection("devl")
        self._test_table = CategoriesTable(self._database_connection)

    @function_wrapper
    def test_1_select(self):
        self._test_table.truncate()
        category_name = "TestCat_1"
        missing_id = self._test_table.select_by_name(category_name)
        self.assertIsNone(missing_id)

    def test_2_insert(self):
        self._test_table.truncate()
        category_name = "TestCat_2"
        missing_id = self._test_table.select_by_name(category_name)
        self.assertIsNone(missing_id)
        inserted_id = self._test_table.insert(category_name)
        self.assertIsNotNone(inserted_id)
        selected_id = self._test_table.select_by_name(category_name)
        self.assertEqual(inserted_id, selected_id)

    def test_3_update(self):
        category_name = "TestCat_3"
        new_name = "TestCat_3_updated"
        selected_id = self._test_table.select_by_name(category_name)
        self.assertIsNone(selected_id)
        inserted_id = self._test_table.insert(category_name)
        self.assertIsNotNone(inserted_id)
        self._test_table.update_by_id(inserted_id, new_name)
        selected_id = self._test_table.select_by_name(category_name)
        self.assertIsNone(selected_id)
        selected_id = self._test_table.select_by_name(new_name)
        self.assertEqual(inserted_id, selected_id)

    def test_4_delete(self):
        category_name = "TestCat_4"
        selected_id = self._test_table.select_by_name(category_name)
        self.assertIsNone(selected_id)
        inserted_id = self._test_table.insert(category_name)
        self.assertIsNotNone(inserted_id)
        rows_deleted = self._test_table.delete_by_id(inserted_id)
        self.assertEqual(rows_deleted, 1)
        selected_id = self._test_table.select_by_name(category_name)
        self.assertIsNone(selected_id)

    def tearDown(self):
        self._test_table.truncate()
        self._test_table = None
        self._database_connection = None


if __name__ == "__main__":
    unittest.main()


"""
        self.fail("Finish the test_2_add test")
class FilesProcessedTest(unittest.TestCase):
    def setUp(self):
        self.stage_dir = Path("/Users/jeff/devl/TROLoad/stage")
        self.test_file = Path(f"{self.stage_dir}/test_file.csv")
        self.test_file.write_text("category name, hidden")
        self.test_file.write_text("test cat, False")

    def test_no_remaining_csv_files(self):
        try:
            this_app = TroLoadApp("troload", "0.0.0")
            rc = this_app.process()
            this_app.destruct(rc)
            print(f"The syspath - {sys.path}")
        except Exception as e:
            print(f"Following uncaught exception occured. {e}")

        files = self.stage_dir.glob("*.csv")

        for i in files:
            self.fail(f"The file {i} still exist in the stage directory")

    def tearDown(self):
        self.test_file.unlink()
"""
