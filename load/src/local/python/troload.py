'''
troload - Load Excel spreadsheet from Quicken into the Postgres TRO database.
'''
import argparse
import config
import glob
import logging
import openpyxl
import os
import sys
from time import sleep

# from psycopg2.extensions import TRANSACTION_STATUS_IDLE

import accounts as accts
import categories as cat
import transactions as trans

import modules.jsstdrpt as rpt
import modules.jspgeng as eng
#
#  Global variables
connection = None


def my_startup(log_level, home_dir, environment):
    global connection

    if log_level == 'DEBUG':
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            handlers=[logging.StreamHandler(), logging.FileHandler(filename='troload.log')]
                            )
    else:
        if log_level == 'INFO':
            logging.basicConfig(level=logging.INFO,
                                format='%(asctime)s %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S',
                                handlers=[logging.StreamHandler(), logging.FileHandler(filename='troload.log')]
                                )

    connection = eng.pg_get_connection(host='pgpods-server', database=environment, username='tro_rw', password=f'tro_rw_{environment}')
    connection.autocommit = True

    output_dir = rpt.make_std_out_dir(home_dir + '/local/rpt')
    rpt.start_std_rpt(output_dir, "TROLoad", version="0.1.1")
    rpt.write('TROLoad is starting...\n')


def my_shutdown(rc=0, sysout=None, syserr=None, gword=None):
    rpt.finish_std_rpt(rc)
    logging.info("troload is ending...")
    sys.stdout.flush()
    sys.exit(rc)


def get_cmdline_args():
    parser = argparse.ArgumentParser(description="TROLoad")
    parser.add_argument(
        "-e", "--environment",
        required=True,
        help="Environment - devl, test or prod"
    )
    args = parser.parse_args()
    return args


def get_next_file(stage_dir):
    logging.debug(f'begin get_next_file({stage_dir})')
    file_name = None

    my_path = str(f'{stage_dir}/*.xlsx')
    for file in glob.glob(my_path, recursive=False):
        file_name = f'{file}'

    logging.debug(f'end   get_next_file - retuns {file_name}')
    return file_name


def process_file(file_name):
    global connection
    logging.debug(f'begin process_file({file_name})')

    workbook = openpyxl.load_workbook(filename=file_name)

    accts.load_new_accounts_from_workbook(connection, workbook)
    cat.load_new_categories_from_workbook(connection, workbook)
    trans.load_transactions_from_workbook(connection, workbook)

    new_file_name = f'{file_name}.bkp'
    os.rename(file_name, new_file_name)
    logging.debug('end   process_file - returns None')


def main():
    config_file = './local/etc/troload.cfg'
    my_config = config.Config(config_file)
    log_level = my_config['devl.log_level']
    home_dir = my_config['devl.home_dir']

    comandline_arguments = get_cmdline_args()
    environment = comandline_arguments.environment

    my_startup(log_level, home_dir, environment)

    stage_dir = 'local/stage'
    file_name = get_next_file(stage_dir)
    if file_name is not None:
        process_file(file_name)
    else:
        logging.info("No new files were found")
        rpt.write("No new files were found\n")
    sleep(3600)
    my_shutdown(0)


if __name__ == "__main__":
    main()
