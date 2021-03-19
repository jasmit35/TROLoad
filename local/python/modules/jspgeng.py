#!/usr/bin/env python
"""
jspgeng
"""
import logging
import sqlalchemy as sqla

jspgeng_version = "1"


def pg_get_engine(
    host="localhost", database="pgdb", username="jeff", password="password"
):
    logging.debug("begin pg_get_engine({}, {}, {})".format(host, database,
                  username))

    connstr = "postgresql+psycopg2://{}:{}@{}:5432/{}".format(
        username, password, host, database)
    engine = sqla.create_engine(connstr)

    logging.debug("end   pg_get_engine - returns {}".format(engine))
    return engine
