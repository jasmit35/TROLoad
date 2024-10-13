"""
TROLoad Import data in variosus formats into the TRO database.
"""

import os
from sys import path as PATH
from time import sleep

# Add TROLoads code to the path
code_path = os.path.abspath("./python")
PATH.append(code_path)

# Add TRO code to the path
code_path = os.path.abspath("../tro/python")
PATH.append(code_path)

# Add my standard code to the path
code_path = os.path.abspath("../local/python")
PATH.append(code_path)

from argparse import ArgumentParser
from logging import getLogger
from pathlib import Path
from traceback import print_exc

from __init__ import __version__
from categories_CSV_processor import CategoriesCSVProcessor
from std_app import StdApp
from std_dbconn import get_database_connection
from std_logging import function_logger
from std_report import StdReport
from transactions import TransactionsTable
from transactions_excel_processor import TransactionsExcelProcessor


#  =============================================================================
class TroLoadApp(StdApp):
    #  -----------------------------------------------------------------------------
    def __init__(self, app_name, version):
        super().__init__(app_name, version)
        self._logger = getLogger()

        self._max_return_code = 0

        environment = self.cmdline_params.get("environment")
        self._db_conn = get_database_connection(environment)

        self.output_report = StdReport("TROLoad", __version__, rpt_file_path="reports/TROLoad.rpt")
        self.output_report.print_header()

    # ---------------------------------------------------------------------------------------------------------------------
    def __str__(self):
        return "TroLoadApp"

    __repr__ = __str__

    #  -----------------------------------------------------------------------------
    def report(self, msg):
        self.output_report.report(msg)

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
            "-t",
            "--type",
            required=True,
            choices=["cat", "tran"],
            help="Type of the file being loaded - cat for categories, tran for transactions",
        )
        parser.add_argument(
            "-c",
            "--cfgfile",
            required=False,
            default="etc/troload.cfg",
            help="Name of the configuration file to use",
        )
        args = parser.parse_args()
        return vars(args)

    #  -----------------------------------------------------------------------------
    # Process all files in the stage directory
    @function_logger
    def process(self):
        while(True):
            files_processed = 0

            stage_dir = self.cfg_file_params.get("stage_dir", "stage")
            stage_dir_path = Path(stage_dir)

            for stage_file in stage_dir_path.iterdir():
                files_processed += 1
                rc = self.dispatch_file(stage_file)
                if int(rc) > self._max_return_code:
                    self._max_return_code = rc

            self.output_report.print_footer(self._max_return_code)
            sleep(300)    

        return self._max_return_code

    #  -----------------------------------------------------------------------------
    # if this is a file we can process, dispatch it to the appropriate processor
    @function_logger
    def dispatch_file(self, file_path):
        suffix = file_path.suffix
        processing_type = self.cmdline_params.get("type")

        if suffix == ".csv" and processing_type == "cat":
            self.report(f"processing file {file_path}\n")
            processor = CategoriesCSVProcessor(self._db_conn, file_path, self.output_report)
            rc = processor.process_categories_file()
            return rc

        if suffix == ".xlsx" and processing_type == "tran":
            self.report(f"processing file {file_path}\n")
            processor = TransactionsExcelProcessor(self._db_conn, file_path, self.output_report)
            rc = processor.process_excel_file()
            return rc

        self.report(f"ignoring file   {file_path}\n")
        return 0

    #  -----------------------------------------------------------------------------
    @function_logger
    def process_excel_file(self, file_path):
        self.report(f"  processing file {file_path}\n")

        tran_tab = TransactionsTable(self._db_conn)
        excel_workbook = TransactionWorkbook(self, file_path)

        rc = 0
        start_date, end_date = excel_workbook.get_transaction_date_range()
        self.report(f"    Transactions start date - {start_date}, end date - {end_date}\n")

        row_count = tran_tab.mark_tranactions_obsolete(start_date, end_date)
        if row_count > 0:
            self.report(f"    {row_count} existing rows in that date range were deleted.")

        excel_workbook.load_new_accounts_from_workbook()
        # excel_workbook.load_new_categories_from_workbook()
        rc = excel_workbook.load_transactions_from_workbook()

        new_file_path = f"{file_path}.bkp"
        file_path.rename(new_file_path)

        return rc


#  =============================================================================
if __name__ == "__main__":
    try:
        this_app = TroLoadApp("TROLoad", __version__)
        this_app.process()
    except Exception as e:
        print(f"Following uncaught exception occured. {e}")
        print_exc()
