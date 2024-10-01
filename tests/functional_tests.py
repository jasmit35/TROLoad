"""
functional_tests.py
"""

import os
from sys import path as search_path

# ----------------------------------------------------------------------------------------------------------------------
# Add this app's code to PATH
code_path = os.path.abspath("./python")
search_path.append(code_path)
# Add the TRO app's code to PATH
code_path = os.path.abspath("../TRO/python")
search_path.append(code_path)
# Add my shred code to PATH
code_path = os.path.abspath("../local/python")
search_path.append(code_path)

# from pathlib import Path
from shutil import copy2 as copy_file
from unittest import TestCase
from unittest import main as unittest_main

from categories_table import CategoriesTable
from category_groups import CategoryGroupsTable
from category_types import CategoryTypesTable
from std_dbconn import get_database_connection
from std_logging import StdLogging, function_logger

# from troload import TroLoadApp


class TestLoadCategories(TestCase):
    # ---------------------------------------------------------------------------------------------------------------------
    def __init__(self, testName):
        super(TestLoadCategories, self).__init__(testName)
        self._logger = StdLogging(f"logs/{__name__}.log")

        self._db_conn = get_database_connection("devl")
        self._categories = CategoriesTable(self._db_conn)
        self._category_groups = CategoryGroupsTable(self._db_conn)
        self._category_types = CategoryTypesTable(self._db_conn)

        self._test_category_name = "Automobiles:Fusion:Gasoline"

    # ---------------------------------------------------------------------------------------------------------------------
    def setUp(self):
        sql = """
            delete from tro.categories;
            delete from tro.category_types;
            delete from tro.category_groups;
            insert into tro.category_types (category_type_id, category_type) values (0, 'Unknown');
            insert into tro.category_groups (category_group_id, category_group) values (0, 'Unknown');
            insert into tro.categories overriding system value values (0, 'Uncategorized', 0, 0);
            select setval('tro.categories_category_id_seq', 1, false);
            select setval('tro.category_types_category_type_id_seq', 1, False);
            select setval('tro.category_groups_category_group_id_seq', 1, False);
        """
        with self._db_conn.cursor() as cursor:
            cursor.execute(sql)

    # ---------------------------------------------------------------------------------------------------------------------
    @function_logger
    def test_1_run_load(self):
        # category does not exist
        test_id = self._categories.select_id_using_name(self._test_category_name)
        self.assertIsNone(test_id)

        # stage file with test category
        source_path = os.path.abspath("./tests/mock_files/categories_test_only.csv")
        destination_path = os.path.abspath("./stage/categories.csv")
        copy_file(source_path, destination_path)

        #  run the app
        os.system("python3 python/troload.py -e devl -t cat > logs/TROLoad.out 2>&1")

        # category now exist
        test_id = self._categories.select_id_using_name(self._test_category_name)
        self.assertIsNotNone(test_id)

    # ---------------------------------------------------------------------------------------------------------------------
    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest_main()
