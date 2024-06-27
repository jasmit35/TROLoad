"""
troload.py
"""

import os
import sys
from argparse import ArgumentParser
from pathlib import Path
from traceback import print_exc

from __init__ import __version__

troload_code_path = os.path.abspath("./python")
sys.path.insert(1, troload_code_path)
from std_app import StdApp
from std_dbconn import get_database_connection
from std_logging import function_logger, get_std_logger
from std_report import StdReport

tro_code_path = os.path.abspath("../tro/local/python")
sys.path.insert(1, tro_code_path)
from categories_CSV_processor import CategoriesCSVProcessor
from transactions import TransactionsTable
from transactions_excel_processor import TransactionWorkbook


#  =============================================================================
class TroLoadApp(StdApp):
    _db_conn = None
    _max_return_code = None

    _report = None
    _logger = None

    #  -----------------------------------------------------------------------------
    def __init__(self, app_name, version):
        super().__init__(app_name, version)
        self._logger = get_std_logger()

        self._max_return_code = 0

        environment = self._cmdline_params.get("environment")
        self._db_conn = get_database_connection(environment)

        self._report = StdReport("TROLoad", __version__, rpt_file_path="reports/troload.rpt")

    #  -----------------------------------------------------------------------------
    def __del__(self):
        self._logger.info("begin 'troload.__del__'")

        self._max_return_code = None
        self._db_conn = None

        self._logger.info("end   'troload.__del__'")
        self._logger = None

        return None

    #  -----------------------------------------------------------------------------
    def report(self, msg):
        self._report.report(msg)

    #  -----------------------------------------------------------------------------
    @function_logger
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
            default="etc/troload.cfg",
            help="Name of the configuration file to use",
        )
        parser.add_argument(
            "-t",
            "--type",
            required=False,
            default="trans",
            help="Type of the file being loaded",
        )
        args = parser.parse_args()
        return vars(args)

    #  -----------------------------------------------------------------------------
    # Process all files in the stage directory
    @function_logger
    def process(self):
        files_processed = 0
        stage_dir = self._cfg_file_params.get("stage_dir")
        stage_dir_path = Path(stage_dir)
        for stage_file in stage_dir_path.iterdir():
            files_processed += 1
            rc = self.dispatch_file(stage_file)
            if int(rc) > self._max_return_code:
                self._max_return_code = rc

        return self._max_return_code

    #  -----------------------------------------------------------------------------
    # if this is a file we can process, dispatch it to the appropriate processor
    @function_logger
    def dispatch_file(self, file_path):
        suffix = file_path.suffix
        if suffix in ("", ".bkp"):
            self.report(f"ignoring file   {file_path}\n")
            return 0

        self.report(f"processing file {file_path}\n")

        if suffix == ".xslx":
            processor = TransactionWorkbook()
            rc = processor.process_excel_file(self, file_path)

        if suffix == ".csv":
            processor = CategoriesCSVProcessor(self._db_conn, file_path, self._report)
            rc = processor.process_categories_file()

        return rc

    #  -----------------------------------------------------------------------------
    @function_logger
    def process_excel_file(self, file_path):
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

        return rc


if __name__ == "__main__":
    try:
        this_app = TroLoadApp("TROLoad", __version__)
        rc = this_app.process()
        this_app = None
    except Exception as e:
        print(f"Following uncaught exception occured. {e}")
        print_exc()
