"""
troloadbank - Import quicken banking transactions into the tro database.
"""

from argparse import ArgumentParser
from pathlib import Path
from traceback import print_exc

from std_app import StdApp
from std_dbconn import get_database_connection  # type: ignore
from std_logging import function_logger
from std_report import StdReport
from bank_trans_proc import TransactionsProcessor


#  =============================================================================
class TroLoadBank(StdApp):
    #  -----------------------------------------------------------------------------
    def __init__(self):
        super().__init__("TROLoadBank", "3.14")
        self._max_return_code = 0

        environment = self.cmdline_params.get("environment")
        if environment not in ["devl", "test", "prod"]:
            raise ValueError(f"Invalid environment - {environment}")

        self._db_conn = get_database_connection(environment)

        self.output_report = StdReport(
            "TRO Load Banking Transactions", self._version, rpt_file_path="reports/TROLoadBank.rpt"
        )
        self.output_report.print_header()
        return

    # ---------------------------------------------------------------------------------------------------------------------
    def __str__(self):
        return "TroLoadTrans"

    __repr__ = __str__

    #  -----------------------------------------------------------------------------
    def report(self, msg):
        self.output_report.report(msg)

    #  -----------------------------------------------------------------------------
    @function_logger
    def set_cmdline_params(self):
        parser = ArgumentParser(description="TROLoadBank")
        parser.add_argument(
            "-e",
            "--environment",
            required=True,
            help="Environment - devl, test or prod",
        )
        parser.add_argument(
            "-s",
            "--start_date",
            required=True,
            help="Date of the earliest transaction.",
           )
        parser.add_argument(
            "-f",
            "--finish_date",
            required=True,
            help="Date of the last transaction.",
        )
        parser.add_argument(
            "-c",
            "--cfgfile",
            required=False,
            default="etc/troloadbank.cfg",
            help="Name of the configuration file to use",
        )
        args = parser.parse_args()
        return vars(args)

    #  -----------------------------------------------------------------------------
    #  Process the
    @function_logger
    def process_all_files(self):
        stage_dir = self.cfg_file_params.get("stage_dir", "stage")
        stage_dir_path = Path(stage_dir)
        self.report(f"processing files in {stage_dir_path}\n")

        for stage_file in stage_dir_path.iterdir():
            if stage_file.suffix != ".xlsx":
                continue
            self.report(f"  processing file {stage_file}\n")

            trans_processor = TransactionsProcessor(self._db_conn, self.output_report, stage_file)
            rc = trans_processor.process_one_file()
            if int(rc) > self._max_return_code:
                self._max_return_code = rc

            new_file_path = f"{stage_file}.bkp"
            stage_file.rename(new_file_path)

        self.output_report.print_footer(self._max_return_code)

        return self._max_return_code


"""    #  -----------------------------------------------------------------------------
     @function_logger
    def process_excel_file(self, file_path):
        self.report(f"  processing file {file_path}\n")

        tran_tab = TransactionsTable(self._db_conn)
        excel_workbook = TransactionsExcelProcessor(self, file_path)

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
 """

#  =============================================================================
if __name__ == "__main__":
    try:
        this_app = TroLoadBank()
        this_app.process_all_files()
    except Exception as e:
        print(f"Following uncaught exception occured. {e}")
        print_exc()
