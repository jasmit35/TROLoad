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
    sql = f"""
        select transaction_id
        from transactions
        where account_fk = '{account_id}'
        and transaction_date = '{transaction_date}'
        and category_fk = '{category_id}'
        and amount = '{amount}'
    """
    result = connection.execute(sql)
    row = result.fetchone()
    if row is None:
        transaction_id = 0
    else:
        transaction_id = row[0]
    return transaction_id


def insert_transaction(connection, account_id, transaction_date, category_id, amount):
    sql = f"""
        insert into transactions (account_fk, transaction_date, category_fk, amount)
        values ({account_id}, '{transaction_date}', {category_id}, {amount})
    """
    connection.execute(sql)


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

    sql = f"""
        update transactions
        set obsolete_date = null,
        cleared = '{cleared}',
        number = '{number}',
        tag = '{tag}',
        description = '{description}',
        memo = '{memo}',
        tax_item = '{tax_item}'
        where transaction_id = {transaction_id}
    """
    connection.execute(sql)


def load_transactions_from_workbook(connection, workbook):
    sheet = workbook.active
    start_date, end_date = get_transaction_date_range(sheet)
    rpt.write(f'\nTransactions start date - {start_date}, end date - {end_date}\n')

    mark_tranactions_obsolete(connection, start_date, end_date)

    #  The spreadsheet we are loading from does not repeat all values for split transactions.
    #  Theirfore it is necessary to retain the previous values.
    previous_transaction_date = None
    previous_account_id = None

    rpt.write("The following transactions have been added:")

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

        if transaction_id == 0:
            insert_transaction(connection, account_id, transaction_date, category_id, amount)
        else:
            update_transaction(connection, transaction_id, value)
