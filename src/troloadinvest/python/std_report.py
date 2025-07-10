"""
std_report.py
"""

import datetime
from logging import getLogger

from std_logging import function_logger


class StdReport:
    #  -----------------------------------------------------------------------------
    def __init__(self, app_name, version="0.0.0", rpt_file_path=None):
        self._logger = getLogger()
        self._logger.info(
            f"Begin 'StdReport.__init__      ' arguments - ({app_name=}, {version=}, {rpt_file_path=})"
        )

        self._app_name = app_name
        self._version = version

        if rpt_file_path:
            self._rpt_file_path = rpt_file_path
        else:
            self._rpt_file_path = self.set_rpt_file_path()

        self._file = open(self._rpt_file_path, "w")
        self._logger.info("End   'StdReport.__init__      ' returns - None")

    # ---------------------------------------------------------------------------------------------------------------------
    def __str__(self):
        return "StdReport"

    # ---------------------------------------------------------------------------------------------------------------------
    __repr__ = __str__

    #  -----------------------------------------------------------------------------
    def __del__(self):
        self._file.close()

    #  -----------------------------------------------------------------------------
    @function_logger
    def _set_cfg_file_params(self):
        return {"home_dir": ".", "stage_dir": "./stage", "log_level": "DEBUG"}

    #  -----------------------------------------------------------------------------
    @function_logger
    def set_rpt_file_path(self):
        today = datetime.datetime.now().strftime("%m_%d_%y_%H_%M")
        file_path = f"logs/{self._app_name}_{today}.rpt"
        return file_path

    #  -----------------------------------------------------------------------------
    def report(self, output_string):
        self._file.write(output_string)

    #  -----------------------------------------------------------------------------
    @function_logger
    def print_header(self):
        start_date = datetime.datetime.now().strftime("%m/%d/%y")
        start_time = datetime.datetime.now().strftime("%H:%M:%S %z")

        self.report(("=" * 132) + "\n")
        self.report(f"{self._app_name}")
        self._file.write(" " * 117)
        self._file.write(f"{start_date}\n")
        self._file.write(f"Version - {self._version}")
        self._file.write(" " * 100)
        self._file.write(f"{start_time}\n")
        self._file.write(("-" * 132) + "\n")

    #  -----------------------------------------------------------------------------
    @function_logger
    def print_footer(self, return_code):
        end_date = datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S %z")

        self._file.write(("-" * 132) + "\n")
        if return_code == 0:
            self.report(f"Finished successfully at {end_date}\n")
        else:
            self.report(f"FAILED! With return code {return_code} at {end_date}\n")

        self.report(("=" * 132) + "\n")

    #  -----------------------------------------------------------------------------
    def get_contents(self):
        self._file.flush()
        with open(self._rpt_file_path) as contents:
            return contents.read()
