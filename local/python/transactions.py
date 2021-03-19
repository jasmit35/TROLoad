'''
transactions
'''
from datetime import date
import logging as log
# import openpyxl


def mark_tranactions_obsolete(db_engine, start_date, end_date):
    todays_date = date.today()
    sql = f"""
        update transactions
        set obsolete_date = '{todays_date}'
        where transaction_date >= '{start_date}'
        and transaction_date <= '{end_date}'
    """
    db_engine.execute(sql)


def validate_transaction(transaction_date, trans_values):
    log.debug(f'Transaction date {transaction_date}')


def load_transactions_from_workbook(db_engine, workbook, output_report):
    output_report.write("The following transactions have been added:")
    sheet = workbook.active
    for value in sheet.iter_rows(
        min_row=3, max_row=3,
        min_col=1, max_col=1,
        values_only=True,
    ):
        date_label = list(value)
        log.debug(f'Date label = {value}')
        date_label = date_label[0].split()
        start_date = date_label[0]
        end_date = date_label[2]
        output_report.write(f'\nTransactions start date - {start_date}, \
            end date - {end_date}\n')
    mark_tranactions_obsolete(db_engine, start_date, end_date)
    previous_date = None
    for value in sheet.iter_rows(
        min_row=8, max_row=999,
        min_col=2, max_col=12,
        values_only=True
    ):
        transaction_date = value[0]
        if transaction_date is None:
            transaction_date = previous_date
        validate_transaction(transaction_date, value)
        previous_date = transaction_date
