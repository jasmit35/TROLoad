'''
transactions
'''
import datetime
import logging as log

import accounts
import categories

import modules.jsstdrpt as rpt


def get_transaction_date_range(sheet):
    log.debug(f'begin get_transaction_date_rangei({sheet})')
    for value in sheet.iter_rows(
        min_row=3, max_row=3,
        min_col=1, max_col=1,
        values_only=True,
    ):
        date_label = list(value)[0].split()
        start_date = date_label[0]
        end_date = date_label[2]
    log.debug(f'end   get_transaction_date_range - returns {start_date}, {end_date}')
    return start_date, end_date


def mark_tranactions_obsolete(connection, start_date, end_date):
    todays_date = datetime.date.today()
    sql = """
        update tro.transactions
        set obsolete_date = %s
        where transaction_date >= %s
        and transaction_date <= %s
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, (todays_date, start_date, end_date))


def get_transaction_id(connection, account_id, transaction_date, category_id, amount):
    log.debug(f'Transaction date {transaction_date}')
    sql = """
        select transaction_id
        from tro.transactions
        where account_fk = %s
        and transaction_date = %s
        and category_fk = %s
        and amount = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, (account_id, transaction_date, category_id, amount))
        row = cursor.fetchone()
    if row is None:
        transaction_id = None
    else:
        transaction_id = row[0]
    return transaction_id


def insert_transaction(connection, account_id, transaction_date, category_id, amount):
    log.debug(f'begin insert_transaction ({account_id}, {transaction_date}, {category_id}, {amount})')
    sql = """
        insert into tro.transactions (account_fk, transaction_date, category_fk, amount)
        values (%s, %s, %s, %s)
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, (account_id, transaction_date, category_id, amount))


def update_transaction(connection, transaction_id, other_values):
    cleared = other_values[9]
    if cleared is None:
        cleared = ''

    description = str(other_values[3]).replace("'", "''")

    tag = other_values[6]
    if tag is None:
        tag = ''

    number = other_values[2]
    memo = other_values[4]
    tax_item = other_values[8]

    sql = """
        update tro.transactions
        set obsolete_date = null,
        cleared = %s,
        number = %s,
        tag = %s,
        description = %s,
        memo = %s,
        tax_item = %s
        where transaction_id = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, (cleared, number, tag, description, memo, tax_item, transaction_id))


def load_transactions_from_workbook(connection, workbook):
    sheet = workbook.active
    start_date, end_date = get_transaction_date_range(sheet)
    rpt.write(f'\nTransactions start date - {start_date}, end date - {end_date}\n')

    mark_tranactions_obsolete(connection, start_date, end_date)

    #  The spreadsheet we are loading from does not repeat all values for split transactions.
    #  Theirfore it is necessary to retain the previous values.
    previous_transaction_date = None
    previous_account_id = None

    rpt.write("\n\n  The following transactions have been added:\n")

    for value in sheet.iter_rows(
        min_row=8, max_row=999,
        min_col=2, max_col=12,
        values_only=True
    ):
        account_name = value[1]
        if account_name is None:
            account_id = previous_account_id
        else:
            account_id = accounts.get_account_id(account_name)
        previous_account_id = account_id

        #  The iterator function picks up rows from the spreadsheet the are not valid.
        #  The easist way to exclude them is to check for a valid trasaction date.
        transaction_date_string = str(value[0])
        if transaction_date_string is None:
            transaction_date = previous_transaction_date
        else:
            try:
                iso_date_string = str(transaction_date_string.split()[0])
                transaction_date = datetime.date.fromisoformat(iso_date_string)
            except ValueError:
                continue
        previous_transaction_date = transaction_date

        category_name = value[5]
        category_id = categories.get_category_id(category_name)

        amount = value[10]

        transaction_id = get_transaction_id(connection, account_id, transaction_date, category_id, amount)

        if transaction_id is None:
            insert_transaction(connection, account_id, transaction_date, category_id, amount)
            rpt.write(f"    {account_name}, {transaction_date}, {category_name}, {amount}\n")
        else:
            update_transaction(connection, transaction_id, value)
