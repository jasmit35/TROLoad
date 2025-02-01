"""
std_dbconn
"""

import configparser

from psycopg2 import OperationalError, connect


def get_database_connection(environment):
    config = configparser.ConfigParser()
    config.read("./etc/.db_secrets.cfg")

    host_name = config[environment]["hostname"]
    host_port = config[environment]["hostport"]
    database = config[environment]["database"]
    username = config[environment]["username"]
    password = config[environment]["password"]

    #  connstr = f"dbname={database} user={username} password={password} host={host_name} port={host_port}"
    connstr = f"dbname={database} user={username} password={password} host={host_name} port={host_port}"

    connection = None
    try:
        connection = connect(connstr)
    except OperationalError as e:
        print(f"Connection error: {e}")

    if connection is not None:
        connection.autocommit = True

    return connection


""" def get_database_connection(environment):
    load_dotenv("./etc/.db_secrets.env")

    host_name = os.getenv(f"{environment}_DB_HOSTNAME".upper())
    host_port = os.getenv(f"{environment}_DB_HOSTPORT".upper())
    database = os.getenv(f"{environment}_DB_DATABASE".upper())
    username = os.getenv(f"{environment}_DB_USERNAME".upper())
    password = os.getenv(f"{environment}_DB_PASSWORD".upper())

    connstr = f"dbname={database} user={username} password={password} host={host} port={port}"

    connection = pg_get_connection(
        host=host_name, port=host_port, database=database, username=username, password=password
    )
    connection.autocommit = True
    return connection


def pg_get_connection(host="localhost", port="5432", database="pgdb", username="jeff", password="password"):
    connstr = f"dbname={database} user={username} password={password} host={host} port={port}"
    connection = None

    try:
        connection = connect(connstr)
    except OperationalError as e:
        print(f"Connection error: {e}")

    return connection
"""
