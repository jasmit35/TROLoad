import os
import sys
import unittest

tro_code_path = os.path.abspath("../tro/local/python")
sys.path.insert(1, tro_code_path)
from categories import CategoriesTable

tro_code_path = os.path.abspath("../local/python")
sys.path.insert(1, tro_code_path)
from std_dbconn import get_database_connection


class TestCategories(unittest.TestCase):
    _database_connection = None
    _test_id = None
    _test_table = None

    def setUp(self):
        environment = "Devl"
        self._database_connection = get_database_connection(environment)
        self._test_table = CategoriesTable(self._database_connection)

    def test_1_category_does_not_exist(self):
        self._test_id = self._test_table.get_id("TestCat", False)
        self.assertIsNone(self._test_id)

    def test_2_add_category(self):
        self.fail("Finish the test_2_add test")

    def test_3_category_exist(self):
        self._test_id = self._test_table.get_id("TestCat", False)
        self.assertEqual(self._test_id, 1)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()


"""
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
