"""
tab_nodes.py
"""
import logging

import modules.tab_regions as m_t_regions


def process_name(db_conn, node_name, processed_date, node_details):
    node_id = select_name(db_conn, node_name)
    if node_id is None:
        #  region_id is a not null column
        region_id = m_t_regions.get_region_for_node(db_conn, node_name)
        insert(db_conn, node_name, region_id, processed_date, node_details)
        node_id = select_name(db_conn, node_name)
    else:
        update(db_conn, node_id, processed_date, node_details)

    return node_id


def select_name(db_conn, node_name):
    logging.info(f"begin nodes_select_name({node_name})")

    sql = f"select node_id from nodes where name like '{node_name}%%'"
    results = db_conn.execute(sql)
    row = results.fetchone()
    if row is None:
        node_id = None
    else:
        node_id = row["node_id"]

    logging.info(f"end   select_name returns - {node_id}")
    return node_id


def insert(self, node_name, region_fk, processed_date, node_details):
    logging.info(f"begin insert_node({node_name}, {region_fk}, \
{processed_date}, {node_details})")

    self.node_name = node_name
    self.populate()

    if self.node_id is None:
        stmt = f"""
            insert into dbsec.nodes (name, region_fk,
                                     lastprocessed, node_details)
            values ('{node_name}', {region_fk},
                    '{processed_date}', '{node_details}')
        """
        logging.debug(f"stmt = {stmt}")
        self.db_conn.execute(stmt)
        self.populate()

    node_id = self.node_id

    logging.info(f"end   insert_node returns - {node_id}")
    return node_id


def update(db_conn, node_id, processed_date, node_details):
    logging.info(f"begin update({node_id}, {processed_date}, \
{node_details})")
    if node_details is None:
        stmt = f"""
            update nodes
               set lastprocessed = '{processed_date}'
             where node_id = {node_id}
        """
    else:
        stmt = f"""
            update nodes
               set lastprocessed = '{processed_date}',
                   details = '{node_details}'
             where node_id = {node_id}
        """
    logging.debug(stmt)
    db_conn.execute(stmt)


# def get_superusers():
#     #  If we have not populated the details attribute, do so
#     if details is None:
#         populate()
#     try:
#         superusers = list(details['superusers'])
#     except Exception as e:
#         superusers = None

#     logging.debug(f"end  get_superusers returns -  {superusers}")
#     return superusers
