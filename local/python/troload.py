"""
troload.py
"""
import os
import sys
from argparse import ArgumentParser

#  from glob import glob
#  from operator import methodcaller
from pathlib import Path
from traceback import print_exc

from __init__ import __version__
from csv_file import CSVFile

shared_code_path = os.path.abspath("../local/python")
sys.path.insert(1, shared_code_path)
from base_app import BaseApp
from std_dbconn import get_database_connection

tro_code_path = os.path.abspath("../tro/local/python")
sys.path.insert(1, tro_code_path)
from transactions import TransactionsTable
from transwkbk import TransactionWorkbook


#  =============================================================================
class TroLoadApp(BaseApp):
    def __init__(self, app_name, version):
        super().__init__(app_name, version)
        self.db_conn = get_database_connection(self.environment)

    #  -----------------------------------------------------------------------------
    def set_cmdline_params(self):
        parser = ArgumentParser(description="TROLoad")
        parser.add_argument(
            "-e",
            "--environment",
            required=True,
            help="Environment - devl, test or prod",
        )
        parser.add_argument(
            "-c",
            "--cfgfile",
            required=False,
            default="troload.cfg",
            help="Name of the configuration file to use",
        )
        args = parser.parse_args()
        return vars(args)

    #  -----------------------------------------------------------------------------
    def process(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        self.info("begin process()")

        max_rc = 0
        files_processed = 0
        stage_dir = self.cfgfile_params.get("stage_dir", "local/stage")
        stage_dir_path = Path(stage_dir)
        for stage_file in stage_dir_path.iterdir():
            files_processed += 1
            rc = self.dispatch_files(stage_file)
            if rc > max_rc:
                max_rc = rc
        return max_rc

        self.info(f"end process - reurns {max_rc}.")

    #  -----------------------------------------------------------------------------
    def dispatch_files(self, file_path):
        """
        Chech extensiton of a file. If we handle it, dispatch to approriate routine.

        Args:
            file_path (_type_): _description_

        Returns:
            _type_: _description_
        """
        self.info(f"begin dispatch_files({file_path})")

        rc = 0
        suffix = file_path.suffix
        if suffix in ("", ".bkp"):
            pass
        elif suffix == ".csv":
            rc = self.process_csv_file(file_path)
        elif suffix == ".xlsx":
            rc = self.process_excel_file(file_path)
        else:
            print(f"suffix type {suffix} not currently handled.")
            rc = 16

        self.info(f"end  dispatch_files - returns {rc}")
        return rc

    #  -----------------------------------------------------------------------------
    def process_csv_file(self, file_path):
        """_summary_

        Args:
            file_path (_type_): _description_
        """
        self.info(f"begin process_csv_file({file_path=})")
        self.output(f"  processing file {file_path}\n")

        CSVFile(file_path)

    #  -----------------------------------------------------------------------------
    def process_excel_file(self, file_path):
        """_summary_

        Args:
            file_path (_type_): _description_
        """
        self.info(f"begin process_excel_file({file_path=})")
        self.output(f"  processing file {file_path}\n")

        tran_tab = TransactionsTable(self.db_conn)
        excel_workbook = TransactionWorkbook(self, file_path)

        rc = 0
        start_date, end_date = excel_workbook.get_transaction_date_range()
        self.output(f"    Transactions start date - {start_date}, end date - {end_date}\n")

        row_count = tran_tab.mark_tranactions_obsolete(start_date, end_date)
        if row_count > 0:
            self.output(f"    {row_count} existing rows in that date range were deleted.")

        excel_workbook.load_new_accounts_from_workbook()
        excel_workbook.load_new_categories_from_workbook()
        rc = excel_workbook.load_transactions_from_workbook()

        new_file_path = f"{file_path}.bkp"
        file_path.rename(new_file_path)

        self.info(f"end   process_excel_file - returns {rc=}")
        return rc


if __name__ == "__main__":
    try:
        this_app = TroLoadApp("troload", __version__)
        rc = this_app.process()
        #         rc = this_app.test_get()
        this_app.destruct(rc)
    except Exception as e:
        print(f"Following uncaught exception occured. {e}")
        print_exc()
