'''
transactions
'''
import datetime
import logging as log
# import openpyxl
import accounts
import categories


def load_transactions_from_workbook(db_engine, workbook, output_report):
    sheet = workbook.active
    start_date, end_date = get_transaction_date_range(sheet)
    output_report.write(f'\nTransactions start date - {start_date}, end date - {end_date}\n')

    mark_tranactions_obsolete(db_engine, start_date, end_date)

    #  The spreadsheet we are loading from does not repeat all values for split transactions.
    #  Theirfore it is necessary to retain the previous values.
    previous_transaction_date = None
    previous_account_id = None

    accounts_dictionary = accounts.select_all_accounts(db_engine)

    output_report.write("The following transactions have been added:")

    for value in sheet.iter_rows(
        min_row=8, max_row=999,
        min_col=2, max_col=12,
        values_only=True
    ):
        account_name = value[1]
        if account_name is None:
            account_id = previous_account_id
        else:
            account_id = accounts_dictionary[account_name]
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

        transaction_id = get_transaction_id(db_engine, account_id, transaction_date, category_id, amount)

        if transaction_id == 0:
            insert_transaction(db_engine, account_id, transaction_date, category_id, amount)
        else:
            update_transaction(db_engine, transaction_id, value)


def get_transaction_date_range(sheet):
    for value in sheet.iter_rows(
        min_row=3, max_row=3,
        min_col=1, max_col=1,
        values_only=True,
    ):
        date_label = list(value)[0].split()
        start_date = date_label[0]
        end_date = date_label[2]
        return start_date, end_date


def mark_tranactions_obsolete(db_engine, start_date, end_date):
    todays_date = datetime.date.today()
    sql = f"""
        update transactions
        set obsolete_date = '{todays_date}'
        where transaction_date >= '{start_date}'
        and transaction_date <= '{end_date}'
    """
    db_engine.execute(sql)


def get_transaction_id(db_engine, account_id, transaction_date, category_id, amount):
    log.debug(f'Transaction date {transaction_date}')
    sql = f"""
        select transaction_id
        from transactions
        where account_fk = '{account_id}'
        and transaction_date = '{transaction_date}'
        and category_fk = '{category_id}'
        and amount = '{amount}'
    """
    result = db_engine.execute(sql)
    row = result.fetchone()
    if row is None:
        transaction_id = 0
    else:
        transaction_id = row[0]
    return transaction_id


def insert_transaction(db_engine, account_id, transaction_date, category_id, amount):
    sql = f"""
        insert into transactions (account_fk, transaction_date, category_fk, amount)
        values ({account_id}, '{transaction_date}', {category_id}, {amount})
    """
    db_engine.execute(sql)


def update_transaction(db_engine, transaction_id, other_values):
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
    db_engine.execute(sql)
