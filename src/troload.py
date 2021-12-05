"""
troload.py
"""
from argparse import ArgumentParser
import glob
import os
from traceback import print_exc
import sys

shared_code_path = os.path.abspath("../local/python")
sys.path.insert(1, shared_code_path)
from std_main import StandardApp

tro_code_path = os.path.abspath("../tro/local/python")
sys.path.insert(1, tro_code_path)
from transactions import TransactionsTable

from transwkbk import TransactionWorkbook

# #  from my standard modules (../local/python)
# p = os.path.abspath("../local/python")
# sys.path.insert(1, p)
# import jspgeng as eng
# import jsstdrpt as rpt

# #  from the TRO application
# p = os.path.abspath("../TRO/local/python")
# sys.path.insert(1, p)
# from transactions import TransactionsTable


def get_cmdline_parms():
    parser = ArgumentParser(description="TROLoad")
    parser.add_argument(
        "-e", "--environment", required=True, help="Environment - devl, test or prod"
    )
    parser.add_argument(
        "-c",
        "--cfgfile",
        required=False,
        default="trorpts.cfg",
        help="Name of the configuration file to use",
    )
    args = parser.parse_args()
    return vars(args)


def get_next_file(this_app, stage_dir):
    this_app.debug(f"begin get_next_file({stage_dir=})")
    file_name = None

    my_path = str(f"{stage_dir}/*.xlsx")
    for file in glob.glob(my_path, recursive=False):
        file_name = f"{file}"

    this_app.debug(f"end   get_next_file - retuns {file_name=}")
    return file_name


# def start_rpt(home_dir):
#     output_dir = rpt.make_std_out_dir(home_dir + "/local/rpt")
#     rpt.start_std_rpt(output_dir, "TROLoad", version="0.1.1")
#     rpt.write("TROLoad is starting...\n")
#     return rpt


# def my_shutdown(rc=0, sysout=None, syserr=None, gword=None):
#     rpt.finish_std_rpt(rc)
#     logging.info("troload is ending...")
#     sys.stdout.flush()
#     sys.exit(rc)


def process_file(this_app, file_name):
    this_app.debug(f"begin process_file({file_name})")

    tran_tab = TransactionsTable(this_app.db_conn)
    excel_workbook = TransactionWorkbook(this_app, file_name)

    start_date, end_date = excel_workbook.get_transaction_date_range()
    this_app.write(f"\nTransactions start date - {start_date}, end date - {end_date}\n")

    tran_tab.mark_tranactions_obsolete(start_date, end_date)

    excel_workbook.load_new_accounts_from_workbook()
    excel_workbook.load_new_categories_from_workbook()
    excel_workbook.load_transactions_from_workbook()

    new_file_name = f"{file_name}.bkp"
    os.rename(file_name, new_file_name)
    this_app.debug("end   process_file - returns None")


def main():
    this_app = StandardApp("troload")

    new_vars = get_cmdline_parms()
    this_app.cmdline_params.update(new_vars)

    rc = 0
    stage_dir = "local/stage"
    file_name = get_next_file(this_app, stage_dir)
    while file_name:
        process_file(this_app, file_name)
        file_name = get_next_file(this_app, stage_dir)
    else:
        this_app.info("No new files were found")
        this_app.write("No new files were found\n")
        rc = 1

    this_app.std_shutdown(rc)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Following uncaught exception occured. {e}")
        print_exc()
