#!/usr/bin/env python
"""
jspgeng
"""
import logging
import psycopg2


def pg_get_connection(host="localhost", database="pgdb", username="jeff", password="password"):
    logging.debug(f"begin pg_get_connection({host}, {database}, {username})")

    connstr = f"dbname={database} user={username} password={password} host={host} port=5432"
    connection = None

    try:
        connection = psycopg2.connect(connstr)
    except psycopg2.OperationalError as ex:
        logging.error(f'Connection failed: {ex}')

    logging.debug(f"end   pg_get_connection - returns {connection}")
    return connection
