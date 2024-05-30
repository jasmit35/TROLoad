import csv
import logging
import os
from pathlib import Path
from sys import path as search_path

code_path = os.path.abspath("../local/python")
search_path.insert(1, code_path)
from function_logger import function_logger

code_path = os.path.abspath("../TRO/local/python")
search_path.insert(1, code_path)
from categories import CategoriesData, CategoriesTable


class CategoriesFileProcessor:

    def __repr__(self) -> str:
        return "CategoriesFileProcessor"

    def __init__(self, db_conn, csv_file_path):
        self._db_conn = db_conn
        self._file_path = csv_file_path
        self._categories_table = CategoriesTable(db_conn)

        self._logger = logging.getLogger()

    # @function_logger
    def process_categories_file(self):
        with open(self._file_path, newline="") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row.__len__() == 0:
                    continue

                category_row = CategoriesData(row)
                category_name = category_row.category_name
                self._logger.debug(f"category_row = {category_row}")

                # if category_name is None:
                #     self._logger.info(f"Skipping row {category_row}")
                #    continue

                if category_name in [None, "", "Category", "Category List", "Type", "Expense"]:
                    # self._logger.info(f"Skipping row {category_row}")
                    continue

                self.process_category_row(category_row)

        self.add_bkp_ext(self._file_path)

    # @function_logger
    def process_category_row(self, category_row):
        category_id = self._categories_table.select_by_name(category_row.category_name)
        if category_id is None:
            self._categories_table.insert_row(category_row)

        """
        print(f"new_data = {new_data}")
        test = new_data.category_name
        print(f"test = {test}")
        test2 = new_data.category_id
        print(f"test2 = {test2}")
        """

    @function_logger
    def add_bkp_ext(self, file_path):
        logger = logging.getLogger()
        file_path = Path(file_path)
        logger.debug(f"file_path = {file_path}")
        backup_path_name = f"{file_path}" + ".bkp"
        backup_path = Path(backup_path_name)
        logger.debug(f"backup_path = {backup_path}")
        file_path.replace(backup_path)


"""
class CategoriesData:6
    category_id: int
    category_name: str
    category_type_fk: int
    category_group_fk: int
    category_description: str
    category_hidden: bool
"""
