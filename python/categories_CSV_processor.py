"""
categories_CSV_processor.py
"""

import os
from csv import reader
from pathlib import Path
from sys import path as PATH

code_path = os.path.abspath("../local/python")
PATH.insert(1, code_path)
from std_logging import function_logger, get_std_logger

code_path = os.path.abspath("../TRO/local/python")
PATH.insert(1, code_path)
from categories_table import CategoriesTable
from category_data import CategoryData
from category_groups import CategoryGroupsTable


# ---------------------------------------------------------------------------------------------------------------------
class CategoriesCSVProcessor:
    _db_conn = None
    _file_path = None
    _categories_table = None
    _previous_category_name = None
    _category_groups_table = None

    _report = None
    _logger = None

    # ---------------------------------------------------------------------------------------------------------------------
    def __init__(self, db_conn, csv_file_path, report):
        self._logger = get_std_logger()
        self._logger.info(f"Begin 'CategoriesCSVProcessor.__init__({db_conn=}, {csv_file_path=}, {report=})")
        self._report = report

        self._db_conn = db_conn
        self._file_path = csv_file_path

        self._categories_table = CategoriesTable(self._db_conn)
        self._category_groups_table = CategoryGroupsTable(self._db_conn)
        self._previous_category_name = ""
        self._logger.info("End   'CategoriesCSVProcessor.__init__' returns - None")
        return None

    # ---------------------------------------------------------------------------------------------------------------------
    def __str__(self):
        return "CategoriesCSVProcessor({_file_path=}, {_categories_table=}, {_previous_category_name=})"

    # ---------------------------------------------------------------------------------------------------------------------
    def report(self, msg):
        self._report.report(msg)

    # ---------------------------------------------------------------------------------------------------------------------
    @function_logger
    def process_categories_file(self):
        rc = 0
        with open(self._file_path, newline="") as csv_file:
            file_reader = reader(csv_file)
            for row in file_reader:
                if row.__len__() > 0:
                    category_name = row[0]
                    if category_name in [None, "", "Category", "Category List", "Type", "Expense"]:
                        self.report(f"   Skipping row: {category_name}\n")
                    else:
                        rc = self.process_category_row(row)

        self.add_bkp_ext(self._file_path)
        return rc

    # ---------------------------------------------------------------------------------------------------------------------
    @function_logger
    def process_category_row(self, category_row):
        rc = 0
        new_category_name = self.transform_category_name(category_row[0])

        self._previous_category_name = new_category_name

        category_data = CategoryData(new_category_name)
        category_data.category_type_fk = self.get_category_type_fk(category_row[1])
        category_data.category_group_fk = self.get_category_group_fk(category_row[2])
        category_data.category_description = category_row[3]
        category_data.category_hidden = category_row[4]

        category_id = self._categories_table.select_id_using_name(new_category_name)
        if category_id is None:
            self.report(f"   Inserting {category_data}\n")
            rc = self._categories_table.insert(category_data)
        else:
            category_data.category_id = category_id
            sql = """
                select * from tro.categories
                where category_id = %s
            """
            with self._db_conn.cursor() as cursor:
                cursor.execute(sql, (category_id,))
                existing_row = cursor.fetchone()
                self._logger.debug(f"     {existing_row=}")

            apply_updates = False
            if existing_row[1] != category_data.category_name:
                self.report("    changing '{existing_row[1]}' to '{category_data.category_name}'")
                apply_updates = True

            if existing_row[2] != category_data.category_type_fk:
                self.report("    changing '{existing_row[2]}' to '{category_data.category_type_fk}'")
                apply_updates = True

            if existing_row[3] != category_data.category_group_fk:
                self.report("    changing '{existing_row[3]}' to '{category_data.category_group_fk}'")
                apply_updates = True

            if apply_updates:
                rc = self._categories_table.update(category_id, category_data)

        return rc

    # ---------------------------------------------------------------------------------------------------------------------
    @function_logger
    def transform_category_name(self, category_name):
        new_category_name = category_name
        leading_spaces = len(new_category_name) - len(new_category_name.lstrip())
        if leading_spaces > 0:
            # self._logger.debug(f"    {leading_spaces=}")
            parent_category_names = self._previous_category_name.split(":")
            if leading_spaces == 3:
                new_category_name = parent_category_names[0] + ":" + new_category_name.lstrip()
            if leading_spaces == 6:
                new_category_name = (
                    parent_category_names[0] + ":" + parent_category_names[1] + ":" + new_category_name.lstrip()
                )
            if leading_spaces == 9:
                new_category_name = (
                    parent_category_names[0]
                    + ":"
                    + parent_category_names[1]
                    + ":"
                    + parent_category_names[2]
                    + ":"
                    + new_category_name.lstrip()
                )
            if leading_spaces not in [3, 6, 9]:
                raise ValueError(f"Unexpected leading_spaces = {leading_spaces}")
        return new_category_name

    # ---------------------------------------------------------------------------------------------------------------------
    @function_logger
    def get_category_type_fk(self, category_type):
        return 0

    # ---------------------------------------------------------------------------------------------------------------------
    @function_logger
    def get_category_group_fk(self, category_group):
        if category_group in [None, ""]:
            return 0
        category_group_id = self._category_groups_table.select_id_using_name(category_group)
        if category_group_id is None:
            self.report(f"      Inserting category group '{category_group}'\n")
            category_group_id = self._category_groups_table.insert(category_group)
        return category_group_id

    # ---------------------------------------------------------------------------------------------------------------------
    @function_logger
    def add_bkp_ext(self, file_path):
        file_path = Path(file_path)
        # self._logger.debug(f"file_path = {file_path}")
        backup_path_name = f"{file_path}" + ".bkp"
        backup_path = Path(backup_path_name)
        # self._logger.debug(f"backup_path = {backup_path}")
        file_path.replace(backup_path)
