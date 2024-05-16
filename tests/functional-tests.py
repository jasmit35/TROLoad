import os
import sys
import unittest

tro_code_path = os.path.abspath("../local/python")
sys.path.insert(1, tro_code_path)

tro_code_path = os.path.abspath("../TRO/local/python")
sys.path.insert(1, tro_code_path)

code_path = os.path.abspath("../TROLoad/local/python")
sys.path.insert(1, code_path)

"""
class TestLoadCategories(unittest.TestCase):
    _database_connection = None
    _test_table = None
    _test_category_name = 'test:test:test'

    def __init__(self, testName):
        super(TestLoadCategories, self).__init__(testName)

    def setUp(self):
        self._database_connection = get_database_connection('devl')
        self._test_table = CategoriesTable(self._database_connection)

    def test_1_run_load(self):
        # category does not exist
        test_id = self._test_table.select_by_name(self._test_category_name)
        self.assertIsNone(test_id)
        # stage file with test category
        source_path = Path('./tests/mock_files/categories.csv')
        destination_path = Path('./stage/categories.csv')
        copy(source_path, destination_path)
        # run the load code
        try:
            # this_app = TroLoadApp('troload', 'x.x.0')
            # rc = this_app.process()
            # this_app.destruct(rc)
            troload
        except Exception as e:
            print(f"Following uncaught exception occured. {e}")
            print_exc()
        # category exist
        test_id = self._test_table.select_by_name(self._test_category_name)
        self.assertIsNotNone(test_id)

    def tearDown(self):
        self._test_id = None
        self._test_table = None
        self._database_connection = None
"""

if __name__ == "__main__":
    unittest.main()
