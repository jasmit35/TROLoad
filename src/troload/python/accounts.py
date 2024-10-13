"""
accounts
"""

import os
import sys
from dataclasses import dataclass

code_path = os.path.abspath("../tro/python")
sys.path.append(code_path)

code_path = os.path.abspath("../local/python")
sys.path.append(code_path)


@dataclass
class Account:
    account_id: int
    account_name: str


class AccountsTable:
    def __init__(self, db_conn) -> None:
        self.db_conn = db_conn
        self.existing_accounts = {}
        self.load_existing()

    #  ----------------------------------------------------------------------
    def load_existing(self):
        sql = """
            select account_name, account_id
            from tro.accounts
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
        self.existing_accounts = dict(results)

    #  ----------------------------------------------------------------------
    def get_id(self, account_name, insert_missing=True):
        account_id = self.existing_accounts.get(account_name)
        if insert_missing is False:
            return account_id
        if account_id is None:
            account_id = self.select_id(account_name)
            if account_id is None:
                account_id = self.insert_name(account_name)
            self.existing_accounts[account_name] = account_id
        return account_id

    #  ----------------------------------------------------------------------
    def select_id(self, account_name):
        sql = """
            select account_id
            from tro.accounts
            where account_name = %s
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(sql, (account_name,))
            results = cursor.fetchone()
        if results is None:
            account_id = None
        else:
            account_id = results[0]
        return account_id

    #  ----------------------------------------------------------------------
    def insert_name(self, account_name):
        sql = "insert into tro.accounts (account_name) values (%s)"
        with self.db_conn.cursor() as cursor:
            cursor.execute(sql, (account_name,))

        account_id = self.select_id(account_name)
        return account_id

    #  ----------------------------------------------------------------------
    def select_all_accounts(self):
        sql = """
            select account_name, account_id
            from tro.accounts
            order by account_name
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
        accounts = dict(results)
        return accounts
