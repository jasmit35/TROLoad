"""
std_dbconn
"""

import os

import psycopg2
from dotenv import load_dotenv


def get_database_connection(environment):
    load_dotenv("./etc/.db_secrets.env")
    host_name = os.getenv(f"{environment}_DB_HOSTNAME".upper())
    host_port = os.getenv(f"{environment}_DB_HOSTPORT".upper())
    database = os.getenv(f"{environment}_DB_DATABASE".upper())
    username = os.getenv(f"{environment}_DB_USERNAME".upper())
    password = os.getenv(f"{environment}_DB_PASSWORD".upper())
    connection = pg_get_connection(
        host=host_name, port=host_port, database=database, username=username, password=password
    )
    connection.autocommit = True
    return connection


def pg_get_connection(host="localhost", port="5432", database="pgdb", username="jeff", password="password"):
    connstr = f"dbname={database} user={username} password={password} host={host} port={port}"
    connection = None

    try:
        connection = psycopg2.connect(connstr)
    except Exception:
        raise

    return connection
