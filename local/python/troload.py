'''
troload - Load Excel spreadsheet from Quicken into the Postgres TRO database.
'''

# import subprocess
import argparse
import config
import logging as log
import openpyxl
import sys
from pathlib import Path

import accounts as accts
import categories as cat
import transactions as trans

import modules.jsstdrpt as rpt
import modules.jspgeng as eng
# import run_shell_cmds as rsc


def get_config():
    parser = argparse.ArgumentParser(description="TROLoad")
    parser.add_argument(
        "-e", "--environment",
        required=True,
        help="Environment - devl, test or prod"
    )
    args = parser.parse_args()
    return args


def std_begin(log_level, home_dir):
    if log_level == 'DEBUG':
        my_level = log.DEBUG
    else:
        if log_level == 'INFO':
            my_level = log.INFO

    log.basicConfig(level=my_level, handlers=[log.StreamHandler()])
    log.info("troload is starting...")
    output_dir = rpt.make_std_out_dir(home_dir + '/local/log')
    rpt.start_std_rpt(output_dir, "TROLoad", version="0.1.1")


def std_end(rc=0, sysout=None, syserr=None, gword=None):
    rpt.finish_std_rpt(rc)
    log.info("troload is ending...")
    log.shutdown()
    sys.stdout.flush()
    sys.exit(rc)


def main():
    comandline_arguments = get_config()
    environment = comandline_arguments.environment
    config_file = f'{Path.home()}/{environment}/TROLoad/local/etc/troload.cfg'
    my_config = config.Config(config_file)
    log_level = my_config['devl.log_level']
    home_dir = my_config['devl.home_dir']
    std_begin(log_level, home_dir)

    my_eng = eng.pg_get_engine(database='tro', username='tro',
                               password='trotest')

    workbook_file = f'{Path.home()}/{environment}/TROLoad/local/tmp/Transaction Test.xlsx'
    workbook = openpyxl.load_workbook(
        filename=workbook_file
    )
    accts.load_new_accounts_from_workbook(
        my_eng,
        workbook,
        rpt
    )
    cat.load_new_categories_from_workbook(
        my_eng,
        workbook,
        rpt
    )
    trans.load_transactions_from_workbook(
        my_eng,
        workbook,
        rpt
    )

    rc = 0

    std_end(rc)


if __name__ == "__main__":
    main()
