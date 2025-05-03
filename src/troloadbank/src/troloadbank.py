"""
troloadbank - Import quicken banking transactions into the tro database.
"""

from argparse import ArgumentParser
from pathlib import Path
from traceback import print_exc

from bank_transactions_processor import BankTransactionsProcessor
from std_app import StdApp
from std_dbconn import get_database_connection  # type: ignore
from std_logging import function_logger
from std_report import StdReport


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
            required=False,
            help="Date of the earliest transaction.",
           )
        parser.add_argument(
            "-f",
            "--finish_date",
            required=False,
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
    def process_stagged_files(self):
        stage_dir = self.cfg_file_params.get("stage_dir", "stage")
        stage_dir_path = Path(stage_dir)
        self.report(f"processing files in {stage_dir_path}\n")

        for stage_file in stage_dir_path.iterdir():
            if stage_file.suffix != ".xlsx":
                self.report(f"  ignoring file {stage_file}\n")
                continue
            if stage_file.name[:4] != "bank":
                self.report(f"  ignoring file {stage_file}\n")
                continue
            self.report(f"  processing file {stage_file}\n")

            bank_trans_processor = BankTransactionsProcessor(self._db_conn, self.output_report, stage_file)
            #  start_date = self.cmdline_params.get("start_date")
            #  finish_date = self.cmdline_params.get("finish_date")
            #  rc = trans_processor.process_one_file(start_date, finish_date)
            rc = bank_trans_processor.process_file()
            if int(rc) > self._max_return_code:
                self._max_return_code = rc

            new_file_path = f"{stage_file}.bkp"
            stage_file.rename(new_file_path)

        self.output_report.print_footer(self._max_return_code)

        return self._max_return_code

#  =============================================================================
if __name__ == "__main__":
    try:
        this_app = TroLoadBank()
        this_app.process_stagged_files()
    except Exception as e:
        print(f"Following uncaught exception occured. {e}")
        print_exc()
