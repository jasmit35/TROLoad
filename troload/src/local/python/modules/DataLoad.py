#!/usr/bin/env python
"""
DataLoad.py
"""
import argparse
import json
import logging
import pathlib

import reports.StdReports as r_sr

import modules.jspgeng as eng
import modules.DBSecEnvironment as dbse

import modules.tab_allusers as m_t_allusers
import modules.tab_databases as m_t_databases
import modules.tab_invalidusers as m_t_invalidusers
import modules.tab_nodes as m_t_nodes
import modules.tab_validusers as m_t_validusers

#  Constants and global variables
DATAlOAD_VERSION = "4.2.2"

DBSEC_ENV = None
DBSEC_CONN = None
REPORT = None

DBTYPES_DICT = {}
ALLUSERS_DICT = {}


def get_config():
    logging.info("begin get_config()")

    parser = argparse.ArgumentParser(description="DataLoad")
    parser.add_argument(
        "-e",
        "--environment",
        required=True,
        help="Environment (devl, test, prod)"
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="turn on debug logging",
        required=False,
    )

    args = parser.parse_args()

    logging.info(f"end   get_config() returns - {args.environment}, \
{args.debug}")
    return args.environment, args.debug


# def insert_node(node_name, region_fk, processed_date):
#     logging.info(f"begin insert_node({node_name}, {region_fk}, \
# {processed_date})")
#
#    stmt = f"""
#         insert into dbsec.nodes (name, region_fk, lastprocessed)
#         values ('{node_name}', {region_fk}, '{processed_date}')
#     """
#     logging.debug(f"stmt = {stmt}")
#
#     REPORT.lineout("    Inserting new node")
#     DBSEC_CONN.execute(stmt)
#
#     node_id = select_node(node_name)
#
#     logging.info(f"end   insert_node returns - {node_id}")
#     return node_id


def select_installation(node_fk, dbtype_fk, version):
    sql = f"""
        select installation_id
          from dbsec.installations
         where node_fk = {node_fk}
           and dbtype_fk = {dbtype_fk}
           and version = '{version}'
    """
    try:
        results = DBSEC_CONN.execute(sql)
        row = results.fetchone()
    except Exception as e:
        REPORT.lineout("      " + str(e) + "\n")
        REPORT.lineout("      " + repr(e) + "\n")
        raise e
    if row is None:
        return None
    else:
        return row[0]


def insert_installation(node_fk, dbtype_fk, version):
    sql = f"""
        insert into installations (node_fk, dbtype_fk, version)
        values ({node_fk}, {dbtype_fk}, '{version}')
    """
    DBSEC_CONN.execute(sql)


def process_installations(node_fk, dbtype_fk, version):
    installation_id = select_installation(node_fk, dbtype_fk, version)
    if installation_id is None:
        insert_installation(node_fk, dbtype_fk, version)
        installation_id = select_installation(node_fk, dbtype_fk, version)
    return installation_id


def get_components(node_id):
    stmt = f"""
        select c.name
          from dbsec.nodecomps nc, dbsec.components c
         where nc.comp_fk = c.comp_id
           and nc.node_fk = {node_id}
    """
    results = DBSEC_CONN.execute(stmt)
    component_names = [row[0] for row in results.fetchall()]
    return component_names


def insert_nodecomps(node_id, comp_id):
    stmt = f"""
        insert into dbsec.nodecomps
        values ({node_id}, {comp_id})
    """
    DBSEC_CONN.execute(stmt)


def get_user_id(name):
    logging.info(f"begin get_user_id({name})")

    try:
        user_id = ALLUSERS_DICT.get(name)
    except KeyError:
        user_id, msg = m_t_allusers.process_name(DBSEC_CONN, name)

    if msg is not None:
        REPORT.lineout("  " + msg + "\n")

    logging.info(f"end  get_user_id returns - {user_id}\n")
    return user_id


def get_valid_users(json_data):
    logging.info(f"begin get_valid_users({json_data})")
    #  If the json data has components, use them for valid user ID
    #  identification. If their is not a components key, revert to
    #  using the database types as the "components".
    try:
        component_names = json_data["components"]
    except KeyError:
        component_names = json_data["db_types"]
    except Exception as e:
        REPORT.lineout("      " + str(e) + "\n")
        REPORT.lineout("      " + repr(e) + "\n")
        raise e
    logging.debug("  component_names = " + str(component_names) + "\n")

    valid_users = []
    for component in component_names:
        stmt = f"""
            select au.name
              from allusers au, compusers cu, components c
             where user_id = user_fk
               and comp_id = comp_fk
               and c.name = '{component}'
        """
        results = DBSEC_CONN.execute(stmt)
        for row in results:
            valid_users.append(row[0])
            logging.debug(f"  row[0] - {row[0]}, \
valid_users - str({valid_users})")

    logging.info(f"end  get_valid_users returns - {valid_users}\n")
    return valid_users


def pg_host_data(json_data, node_id):
    try:
        pg_host_data = json_data["pg_host_data"]
    except KeyError:
        REPORT.lineout(f"  No 'pg_host_data' entry in json file.")
        return

    if pg_host_data is None:
        return

    #  Somewhere between python, json and sql the quoting gets messed up
    pg_host_data = str(pg_host_data).replace("'", '"')
    sql = f"""
         update nodes
            set details = '{pg_host_data}'
         where node_id = {node_id}
    """
    DBSEC_CONN.execute(sql)


def process_json_data(json_data):
    logging.info(f"begin process_json_data({json_data})")

    node_name = json_data["hostname"]
    REPORT.lineout(f"  {node_name}\n")
    processed_date = json_data["runtime"]

    if "host_details" in json_data:
        node_details = json_data["host_details"]
    else:
        node_details = None

    node_id = m_t_nodes.process_name(DBSEC_CONN,
                                     node_name,
                                     processed_date,
                                     node_details)

    #  Loop thru the database types on the node
    try:
        db_types = json_data["db_types"]
    except Exception as e:
        REPORT.lineout("      " + str(e) + "\n")
        REPORT.lineout("      " + repr(e) + "\n")
        REPORT.lineout("  This host has no databases")
        return 0

    for db_type in db_types:
        db_type_id = DBTYPES_DICT[db_type]

        valid_users = get_valid_users(json_data)

        #  See if the json data has a list of versions, otherwise unknown.
        try:
            versions = json_data[db_type + "_versions"]
        except KeyError:
            versions = ["unknown"]
            REPORT.lineout(f"  Error! No section {db_type}_versions in json \
file.\n")

        for version in versions:
            installation_id = process_installations(node_id,
                                                    db_type_id,
                                                    version)

            #  Now get the databases using this version
            try:
                databases_dictionary = json_data[str(db_type) + "_databases"]
            except KeyError:
                databases_dictionary = {str(db_type): ["unknown"]}

            #  Get the dictionary that contains the user list for each database
            #  that is using this particular version
            users_dictionary = json_data.get(db_type + "_" + version +
                                             "_users", {})

            #
            #  Get the list of databases that use this version and process
            #  each one
            databases_list = databases_dictionary.get(version, ["unknown"])
            for database in databases_list:
                #  Make sure the database is in our database
                database_id, msg = \
                    m_t_databases.process_databases(DBSEC_CONN,
                                                    installation_id,
                                                    database)
                if msg is not None:
                    REPORT.lineout(f"      {msg}\n")

                #  Get the list of users of it from the dictionary
                #  Then process each one
                users_list = users_dictionary.get(database, ["unknown"])
                for user in users_list:
                    if user in valid_users:
                        msg = m_t_validusers.process_name(DBSEC_CONN,
                                                          user,
                                                          database_id,
                                                          processed_date)
                    else:
                        msg = m_t_invalidusers.process_name(DBSEC_CONN,
                                                            user,
                                                            database_id,
                                                            processed_date)

                    if msg is not None:
                        REPORT.lineout(f"      " + msg + "\n")

        if db_type in ("postgres", "_postgres"):
            pg_host_data(json_data, node_id)


def process_staged_files(stage_dir):
    logging.info(f"begin process_staged_files({stage_dir})")

    #  Loop thru each JSON file in the stage directory
    REPORT.lineout("\nLoading data for nodes:\n")
    stage_dir = pathlib.Path(stage_dir)
    for filename in sorted(stage_dir.glob("*.json")):
        logging.debug(f"  Start processing file {filename}\n")
        #  Parse the JSON data from the file
        #  If it is a zero length file, nothing to process
        file = filename.open()
        file_text = file.read()
        if file_text == "":
            filename.unlink()
            continue

        try:
            json_data = json.loads(file_text)
        except Exception as e:
            REPORT.lineout("      " + str(e) + "\n")
            REPORT.lineout("      " + repr(e) + "\n")
            REPORT.lineout("Error! File {filename} contains invalid JSON \
data.\n")
            continue

        process_json_data(json_data)

        #  Done with this file.
        filename.unlink()  # Remove the processed file

    logging.info("end   process_staged_files - returns 0")
    return 0


def main():
    global DBSEC_ENV
    global DBSEC_CONN
    global REPORT

    global DBTYPES_DICT
    global ALLUSERS_DICT

    logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])
    logging.info("begin main()")

    environment, debug = get_config()

    if debug:
        logging.getLogger().setLevel(logging.DEBUG)

    DBSEC_ENV = dbse.DBSecEnvironment(environment)

    output_dir = DBSEC_ENV.os_user_home + "/local/log"
    REPORT = r_sr.BaseReport("DataLoad", output_dir)
    REPORT.start(" - version: " + DATAlOAD_VERSION)

    db_engine = eng.pg_get_engine(database=DBSEC_ENV.db_name,
                                  username=DBSEC_ENV.db_user)
    DBSEC_CONN = db_engine.connect()
    DBSEC_CONN.execute("set search_path to dbsec,stage,public")

    #  Build a global dictionary to look up dbtype_id bases on the type name
    stmt = "select name, dbtype_id from dbsec.dbtypes"
    results = DBSEC_CONN.execute(stmt)
    [DBTYPES_DICT.update({row["name"]: str(row["dbtype_id"])})
        for row in results]

    #  Build the global list of all users so that we don't repeatedly
    #  query them
    stmt = "select user_id, name from allusers"
    results = DBSEC_CONN.execute(stmt)
    [ALLUSERS_DICT.update({row["name"]: str(row["user_id"])})
        for row in results]

    return_code = process_staged_files(DBSEC_ENV.os_user_home + "/local/stage")

    REPORT.finish(return_code)

    if environment == "prod":
        REPORT.email("js8335@att.com", "DBSec - DataLoad Report")

    logging.info(f"end   main - returns {return_code}")
    exit(return_code)


if __name__ == "__main__":
    main()
