import os
from sys import path as search_path

code_path = os.path.abspath("../local/python")
search_path.insert(1, code_path)
from function_logger import function_logger

code_path = os.path.abspath("../TRO/local/python")
search_path.insert(1, code_path)
from categories import CategoriesTable


class CSVProcessor:

    def __init__(self, db_conn, file_path):
        self._db_conn = db_conn
        self._CategoriesTable = CategoriesTable(self._db_conn)
        self._file_path = file_path

    @function_logger
    def process(self):
        self._CategoriesTable.insert("test:test:test")
        return 0
