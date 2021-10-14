'''
troload - Load Excel spreadsheet from Quicken into the Postgres TRO database.
'''
import argparse
import config
import glob
import logging
import os
import sys

import transactions as trans
from transwkbk import TransactionWorkbook


import modules.jsstdrpt as rpt
import modules.jspgeng as eng


def get_cmdline_parms():
    parser = argparse.ArgumentParser(description="TROLoad")
    parser.add_argument(
        "-e", "--environment",
        required=True,
        help="Environment - devl, test or prod"
    )
    args = parser.parse_args()
    return vars(args)


def get_cfgfile_parms(environment):
    cfgfile = 'local/etc/troload.cfg'
    cfgfile_all_parms = config.Config(cfgfile)
    return cfgfile_all_parms[environment]


def start_log(log_level):
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
    return logging


def start_rpt(home_dir):
    output_dir = rpt.make_std_out_dir(home_dir + '/local/rpt')
    rpt.start_std_rpt(output_dir, "TROLoad", version="0.1.1")
    rpt.write('TROLoad is starting...\n')
    return rpt


def get_database_connection(environment, db_host):
    connection = eng.pg_get_connection(host=db_host,
                                       database=environment,
                                       username='tro_rw',
                                       password=f'tro_rw_{environment}')
    connection.autocommit = True
    return connection


def my_shutdown(rc=0, sysout=None, syserr=None, gword=None):
    rpt.finish_std_rpt(rc)
    logging.info("troload is ending...")
    sys.stdout.flush()
    sys.exit(rc)


def get_next_file(stage_dir):
    logging.debug(f'begin get_next_file({stage_dir})')
    file_name = None

    my_path = str(f'{stage_dir}/*.xlsx')
    for file in glob.glob(my_path, recursive=False):
        file_name = f'{file}'

    logging.debug(f'end   get_next_file - retuns {file_name}')
    return file_name


def process_file(file_name, log, rpt, db_conn):
    logging.debug(f'begin process_file({file_name})')

    excel_workbook = TransactionWorkbook(file_name, log, rpt, db_conn)

    start_date, end_date = excel_workbook.get_transaction_date_range()
    log.debug(f'end   get_transaction_date_range - returns {start_date}, {end_date}')
    rpt.write(f'\nTransactions start date - {start_date}, end date - {end_date}\n')

    trans.mark_tranactions_obsolete(db_conn, start_date, end_date)
    excel_workbook.load_new_accounts_from_workbook()
    excel_workbook.load_new_categories_from_workbook()
    excel_workbook.load_transactions_from_workbook()

    new_file_name = f'{file_name}.bkp'
    os.rename(file_name, new_file_name)
    logging.debug('end   process_file - returns None')


def main():
    cmdline_parms = get_cmdline_parms()

    environment = cmdline_parms["environment"]
    cfgfile_parms = get_cfgfile_parms(environment)

    log_level = cfgfile_parms['log_level']
    log = start_log(log_level)

    home_dir = cfgfile_parms['home_dir']
    rpt = start_rpt(home_dir)

    db_host = cfgfile_parms['database_host']
    db_conn = get_database_connection(environment, db_host)

    stage_dir = 'local/stage'
    file_name = get_next_file(stage_dir)
    if file_name:
        process_file(file_name, log, rpt, db_conn)
    else:
        logging.info("No new files were found")
        rpt.write("No new files were found\n")
    my_shutdown(0)


if __name__ == "__main__":
    main()
