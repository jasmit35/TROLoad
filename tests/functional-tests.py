import os
import sys
import unittest

tro_code_path = os.path.abspath("../tro/local/python")
sys.path.insert(1, tro_code_path)
from categories import CategoriesTable


class TestCategories(unittest.TestCase):
    _test_table = None
    _test_id = None

    def setUp(self):
        self._test_table = CategoriesTable()

    def test_1_category_does_not_exist(self):
        self._test_id = self._test_table.get_id("[401k jeff]:Transfer", False)
        self.assertIsNone(self._test_id)

    def test_2_run_load(self):
        self.fail("Finish the test_2_run_load test")

    def test_3_category_exist(self):
        self._test_id = self._test_table.get_id("[401k jeff]:Transfer", False)
        self.assertEquals(self._test_id, 1)

    def tearDown(self):
        self._test_table = None


if __name__ == "__main__":
    unittest.main()
