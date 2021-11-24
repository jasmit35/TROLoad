"""
main.py
"""

import sys
from traceback import print_exc

#  Imports from my standard library
from std_dbconn import get_database_connection
import std_logging
from std_params import get_cmdline_parms, get_cfgfile_parms

import this_app


def main():
    cmdline_params = get_cmdline_parms()
    environment = cmdline_params.get('environment', 'devl')

    cfgfile_params = get_cfgfile_parms(environment)
    log_level = cfgfile_params.get('log_level', 'debug')
    db_host = cfgfile_params.get('database_host', 'localhost')
    home_dir = cfgfile_params.get('home_dir', None)

    logger = std_logging.start_log(log_level)

    db_conn = get_database_connection(environment)

    rc = this_app(cmdline_params, cfgfile_params, logger, db_conn)

    sys.exit(rc)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Following uncaught exception occured. {e}")
        print_exc()
