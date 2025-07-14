"""
troloadbank - Import quicken banking transactions into the tro database.
"""

import datetime
from argparse import ArgumentParser
from pathlib import Path
from time import sleep
from traceback import print_exc

from bank_transactions_processor import BankTransactionsProcessor
from jasmit_firestarter import StdApp, function_logger
from schedule import every, idle_seconds, run_pending
from std_dbconn import get_database_connection
from std_report import StdReport


#  =============================================================================
class TroLoadBank(StdApp):
    #  -----------------------------------------------------------------------------
    def __init__(self):
        super().__init__("troloadbank")
        self._version = "25.1.0"
        self._max_return_code = 0

        environment = self.cmdline_params.get("environment")
        if environment not in ["devl", "test", "prod"]:
            raise ValueError(f"Invalid environment - {environment}")

        self._db_conn = get_database_connection(environment)
        self._output_report = StdReport("troloadbank", self._version)
        self._stage_dir_path = self.set_stage_dir_path()

        return

    # ---------------------------------------------------------------------------------------------------------------------
    def __str__(self):
        return "TroLoadBank"

    __repr__ = __str__

    #  -----------------------------------------------------------------------------
    def report(self, msg):
        self._output_report.report(msg)

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
    #  Process the files in the stage directory.
    @function_logger
    def process_stagged_files(self):
        file_list = self.filter_list()
        run_time = datetime.datetime.now().strftime("%H:%M")

        if len(file_list) > 0:
            self.report(f"run time : {run_time} - processing files\n")
            for file in file_list:
                self.report(f"    processing file {file}\n")
                bank_trans_processor = BankTransactionsProcessor(self._db_conn, self._output_report, file)
                rc = bank_trans_processor.process_file()

                if rc > self._max_return_code:
                    self._max_return_code = rc

                new_file_path = f"{file}.bkp"
                file.rename(new_file_path)
        else:
            self.report(f"run time : {run_time} - no files to process\n")

        return None

    # -----------------------------------------------------------------------------
    # Extract a list of only the files to process
    @function_logger
    def filter_list(self):
        file_list = []

        for stage_file in self._stage_dir_path.iterdir():
            if stage_file.suffix != ".xlsx":
                continue

            if stage_file.name[:4] != "bank":
                continue

            file_list.append(stage_file)

        return file_list

    # -----------------------------------------------------------------------------
    #
    @function_logger
    def set_stage_dir_path(self):
        stage_dir = "stage"

        cfg_stage_dir = self.cfg_file_params.get("stage_dir")
        if cfg_stage_dir:
            stage_dir = cfg_stage_dir

        stage_dir_path = Path(stage_dir)
        stage_dir_path = stage_dir_path.absolute()

        if not stage_dir_path.exists():
            self.report(f"Stage directory {stage_dir_path} does not exist.\n")
            self._output_report.print_footer(1)
            return None
        if not stage_dir_path.is_dir():
            self.report(f"Stage directory {stage_dir_path} is not a directory.\n")
            self._output_report.print_footer(1)
            return None

        self.report(f"processing files in {stage_dir_path}\n")
        return stage_dir_path


#  =============================================================================
if __name__ == "__main__":
    try:
        this_app = TroLoadBank()

        this_app._output_report.print_header()

        #  every 15 minutes for the next 24 hours process the stagged files
        stop_time = datetime.timedelta(hours=1)
        every(15).minutes.until(stop_time).do(this_app.process_stagged_files)

        while True:
            n = idle_seconds()  # seconds until the next job is due

            if n is None:  # no more jobs to run
                this_app.report("No more jobs to run. Exiting.")
                break

            if n > 0:
                sleep(n)  # sleep until the next job is due
                this_app.report("Running pending jobs...")
                run_pending()

        this_app._output_report.print_footer(this_app._max_return_code)
        final_return_code = this_app._max_return_code

        this_app = None  # clean up

        exit(final_return_code)

    except Exception as e:
        print(f"Following uncaught exception occured. {e}")
        print_exc()
