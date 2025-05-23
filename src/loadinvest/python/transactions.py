"""
transactions
"""

import datetime
import os
import sys
from dataclasses import dataclass

code_path = os.path.abspath("../tro/python")
sys.path.append(code_path)

code_path = os.path.abspath("../local/python")
sys.path.append(code_path)


class InvalidTransactionException(Exception):
    def __init__(self, transaction, message):
        self.transaction = transaction
        self.message = message
        print(message)
        print(transaction)


@dataclass
class Transaction:
    account_fk: int
    transaction_date: datetime.date
    category_fk: int
    amount: float
    cleared: str = ""
    number: str = ""
    tag: str = ""
    description: str = ""
    memo: str = ""
    tax_item: str = ""


class TransactionsTable:
    def __init__(self, db_conn) -> None:
        self.db_conn = db_conn

    def insert_transaction(self, trans) -> None:
        sql = """
            insert into tro.transactions
            (account_fk, transaction_date, category_fk, amount, cleared, number, tag, description, memo, tax_item)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    trans.account_fk,
                    trans.transaction_date,
                    trans.category_fk,
                    trans.amount,
                    trans.cleared,
                    trans.number,
                    trans.tag,
                    trans.description,
                    trans.memo,
                    trans.tax_item,
                ),
            )

    def select_date_range(self, start_date, end_date):
        sql = """
            SELECT account_name,
                '=date(' || TO_CHAR(transaction_date, 'YYYY, MM, DD') || ')',
                description,
                category_name,
                amount,
                cleared,
                number,
                memo,
                tax_item
            FROM tro.accounts, tro.categories, tro.transactions
            WHERE account_id = account_fk
            AND category_id = category_fk
            AND transaction_date BETWEEN %s and %s
            ORDER BY 1, 2, 4, 5;
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(sql, (start_date, end_date))
            return cursor.fetchall()

    #   -----------------------------------------------------------------------------
    def select_date_range_summary(self, start_date, end_date):
        sql = """
            SELECT account_name,
                category_name,
                sum(amount)
            FROM tro.accounts, tro.categories, tro.transactions
            WHERE account_id = account_fk
            AND category_id = category_fk
            AND transaction_date BETWEEN %s and %s
            GROUP BY account_name, category_name
            ORDER BY 1, 2, 3;
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(sql, (start_date, end_date))
            return cursor.fetchall()

    #   -----------------------------------------------------------------------------
    def select_ending_balances(self, end_date):
        sql = """
            SELECT account_name,
                sum(amount)
            FROM tro.accounts, tro.transactions
            WHERE account_id = account_fk
            AND transaction_date <= %s
            GROUP BY account_name
            ORDER BY 1
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(sql, (end_date,))
            return cursor.fetchall()

    #   -----------------------------------------------------------------------------
    # def mark_tranactions_obsolete(self, start_date, end_date):
    #     todays_date = datetime.date.today()
    #     sql = """
    #         update tro.transactions
    #         set obsolete_date = %s
    #         where transaction_date >= %s
    #         and transaction_date <= %s
    #     """
    #     with self.db_conn.cursor() as cursor:
    #         cursor.execute(sql, (todays_date, start_date, end_date))

    def mark_tranactions_obsolete(self, start_date, end_date):
        sql = """
        DELETE FROM tro.transactions
        WHERE transaction_date >= %s
        AND transaction_date <= %s
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(sql, (start_date, end_date))
            return cursor.rowcount

    #   -----------------------------------------------------------------------------
    def get_transaction_id(self, account_id, transaction_date, category_id, amount):
        sql = """
        select transaction_id
        from tro.transactions
        where account_fk = %s
        and transaction_date = %s
        and category_fk = %s
        and amount = %s
    """
        with self.db_conn.cursor() as cursor:
            cursor.execute(sql, (account_id, transaction_date, category_id, amount))
            row = cursor.fetchone()

        transaction_id = None if row is None else row[0]
        return transaction_id

    def update_transaction(self, transaction_id, other_values):
        cleared = other_values[9]
        if cleared is None:
            cleared = ""

        description = str(other_values[3]).replace("'", "''")

        tag = other_values[6]
        if tag is None:
            tag = ""

        number = other_values[2]
        memo = other_values[4]
        tax_item = other_values[8]

        sql = """
            update tro.transactions
            set cleared = %s,
            number = %s,
            tag = %s,
            description = %s,
            memo = %s,
            tax_item = %s
            where transaction_id = %s
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(sql, (cleared, number, tag, description, memo, tax_item, transaction_id))
