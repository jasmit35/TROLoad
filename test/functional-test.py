import os
import sys
import unittest
from pathlib import Path

shared_code_path = os.path.abspath("../local/python")
sys.path.append(shared_code_path)

shared_code_path = os.path.abspath("../TROLoad/local/python")
sys.path.append(shared_code_path)

from troload import TroLoadApp

#  from setuptools import setup, find_packages
#  setup(name = 'troload', packages = find_packages())
#  from '/Users/jeff/devl/TROLoad/local/python' import troload
#  from local.python import troload
#  from local.python.troload import TroLoadApp


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


if __name__ == "__main__":
    unittest.main(warnings="ignore")
