"""
categories_table.py
===================
This module contains the CategoriesTable class which is used to interact with the 'categories' table in the database.

Classes:
    CategoriesTable: This class is used to interact with the 'categories' table in the database.

Methods:
    select_id_using_name: This method is used to select a category_id from the 'categories' table using the category_name.
    insert: This method is used to insert a new row into the 'categories' table.
    update: This method is used to update a row in the 'categories' table.
    delete_by_id: This method is used to delete a row from the 'categories' table using the category_id.
    reset: This method is used to reset the 'categories' table to its initial state.
    get_row_count: This method is used to get the number of rows in the 'categories' table.

"""

import os
import sys
from logging import getLogger

code_path = os.path.abspath("../tro/python")
sys.path.append(code_path)

code_path = os.path.abspath("../local/python")
sys.path.append(code_path)

from std_logging import function_logger


class CategoriesTable:
    # ---------------------------------------------------------------------------------------------------------------------
    def __init__(self, db_conn):
        self._logger = getLogger()
        self._logger.info(f"Begin 'CategoriesTable.__init__' arguments - ({db_conn=})")

        self._db_conn = db_conn

        self._logger.info("End   'CategoriesTable.__init__' returns - None")

    # ---------------------------------------------------------------------------------------------------------------------
    def __str__(self):
        return "CategoriesTable"

    __repr__ = __str__

    # ---------------------------------------------------------------------------------------------------------------------
    @function_logger
    def select_id_using_name(self, category_name):
        category_id = None
        sql = """
            select category_id
            from tro.categories
            where category_name = %s
        """
        with self._db_conn.cursor() as cursor:
            cursor.execute(sql, (category_name,))
            results = cursor.fetchone()
            if results:
                category_id = results[0]

        return category_id

    # ---------------------------------------------------------------------------------------------------------------------
    @function_logger
    def insert(self, category_data):
        sql = """
            insert into tro.categories
            (category_name, category_type_fk, category_group_fk)
            values (%s, %s, %s)
            returning category_id
        """
        with self._db_conn.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    category_data.category_name,
                    category_data.category_type_fk,
                    category_data.category_group_fk,
                ),
            )
            results = cursor.fetchone()
            if results:
                return results

    # ---------------------------------------------------------------------------------------------------------------------
    @function_logger
    def update(self, category_id, category_data):
        sql = """
            update tro.categories
                set category_name = %s,
                    category_type_fk = %s,
                    category_group_fk = %s
            where category_id = %s
            """
        with self._db_conn.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    category_data.category_name,
                    category_data.category_type_fk,
                    category_data.category_group_fk,
                    category_id,
                ),
            )

        return 0

    # ---------------------------------------------------------------------------------------------------------------------
    @function_logger
    def delete_by_id(self, category_id):
        sql = """
            delete from tro.categories
            where category_id = %s
        """
        with self._db_conn.cursor() as cursor:
            cursor.execute(sql, (category_id,))
            rows_deleted = cursor.rowcount

            return rows_deleted == 1

    # ---------------------------------------------------------------------------------------------------------------------
    @function_logger
    def reset(self):
        sql = """
            truncate tro.categories;
            insert into tro.categories OVERRIDING SYSTEM VALUE values (0, 'Uncategorized', 0, 0);
            select setval('tro.categories_category_id_seq', 1, false);
        """
        with self._db_conn.cursor() as cursor:
            cursor.execute(sql)

    # ---------------------------------------------------------------------------------------------------------------------
    @function_logger
    def get_row_count(self):
        sql = """
            select count(*) from tro.categories;
        """
        with self._db_conn.cursor() as cursor:
            cursor.execute(sql)
            row_count = cursor.fetchone()[0]

        return row_count
