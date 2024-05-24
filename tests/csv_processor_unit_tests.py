import logging
import unittest
from os.path import abspath as full_path
from os.path import exists as file_exists
from shutil import copy2 as copy_file
from sys import path as environment_path

# add this project's local python path to the system path
code_path = full_path("./local/python")
environment_path.insert(1, code_path)
from csv_processor import CSVProcessor
from function_logger import function_logger

# add common python library's path to the system path
code_path = full_path("../local/python")
environment_path.insert(1, code_path)
from std_dbconn import get_database_connection

# add TRO's local python path to the system path
code_path = full_path("../tro/local/python")
environment_path.insert(1, code_path)


class CSVProcessorUnitTest(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        logging.basicConfig(
            level=logging.DEBUG,
            filename="CSVProcessorUnitTest.log",
            datefmt="%Y-%m-%d %H:%M:%S",
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self._database_connection = get_database_connection("devl")
        self._test_file = full_path("./local/stage/categories.csv")
        self._cvs_processor = CSVProcessor(self._database_connection, self._test_file)

    @function_logger
    def setUp(self):
        # stage file with test category
        mock_file = full_path("./tests/mock_files/categories.csv")
        copy_file(mock_file, self._test_file)

    @function_logger
    def test_1_file_found_then_renamed(self):
        file_exist = file_exists("./local/stage/categories.csv")
        self.assertTrue(file_exist)
        file_exist = file_exists("./local/stage/categories.csv.bkp")
        self.assertFalse(file_exist)

        self._cvs_processor.process()

        file_exist = file_exists("./local/stage/categories.csv")
        self.assertFalse(file_exist)
        file_exist = file_exists("./local/stage/categories.csv.bkp")
        self.assertTrue(file_exist)

    @function_logger
    def tearDown(self):
        # self._test_table.truncate()
        # self._test_table = None
        # self._database_connection = None
        pass

    @function_logger
    def __del__(self):
        logging.shutdown()


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

"""
        file_handler = logging.FileHandler("CSVProcessorUnitTest.log")
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        self.my_logger.addHandler(file_handler)
"""
