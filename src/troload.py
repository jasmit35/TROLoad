"""
troload.py
"""
from argparse import ArgumentParser
from glob import glob
import os
import sys
from traceback import print_exc

from __init__ import __version__

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
            "-e", "--environment", required=True, help="Environment - devl, test or prod"
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
        self.info('begin process()')
        rc = 0
        stage_dir = "local/stage"
        file_name = self.get_next_file(stage_dir)
        while file_name:
            rc = self.process_file(file_name)
            file_name = self.get_next_file(stage_dir)
        else:
            self.output('No more files were found')
        self.info(f"end  process - returns {rc=}")
        return rc

    #  -----------------------------------------------------------------------------
    def get_next_file(self, stage_dir):
        self.info(f"begin get_next_file({stage_dir=})")
        file_name = None

        my_path = str(f"{stage_dir}/*.xlsx")
        for file in glob(my_path, recursive=False):
            file_name = f"{file}"

        self.info(f"end   get_next_file - retuns {file_name=}")
        return file_name

    #  -----------------------------------------------------------------------------
    def process_file(self, file_name):
        self.info(f"begin process_file({file_name})")
        self.output(f"  processing file {file_name}\n")

        tran_tab = TransactionsTable(self.db_conn)
        excel_workbook = TransactionWorkbook(self, file_name)

        rc = 0
        start_date, end_date = excel_workbook.get_transaction_date_range()
        self.output(f"   Transactions start date - {start_date}, end date - {end_date}\n")

        tran_tab.mark_tranactions_obsolete(start_date, end_date)

        excel_workbook.load_new_accounts_from_workbook()
        excel_workbook.load_new_categories_from_workbook()
        excel_workbook.load_transactions_from_workbook()

        new_file_name = f"{file_name}.bkp"
        os.rename(file_name, new_file_name)
        self.info(f"end   process_file - returns {rc=}")


if __name__ == "__main__":
    try:
        this_app = TroLoadApp("troload", __version__)
        rc = this_app.process()
        this_app.destruct(rc)
    except Exception as e:
        print(f"Following uncaught exception occured. {e}")
        print_exc()
