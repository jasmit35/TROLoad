import os
from sys import path as search_path

code_path = os.path.abspath("../local/python")
search_path.insert(1, code_path)

code_path = os.path.abspath("../TRO/local/python")
search_path.insert(1, code_path)


class CSVProcessor:

    def __init__(self, db_conn, file_path):
        self._db_conn = db_conn
        self._file_path = file_path

    def process(file_path):
        return 0
