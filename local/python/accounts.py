'''
accounts
'''
import logging as log
# import openpyxl

accounts = {}


def select_all_accounts(db_engine):
    sql = """
        select account_name, account_id
        from accounts
        order by account_name
    """
    results = db_engine.execute(sql)
    accounts = {}
    for row in results:
        accounts[row['account_name']] = row['account_id']

    return accounts


def load_new_accounts_from_workbook(db_engine, workbook, output_report):
    global known_accounts
    #  Load the existing accounts
    known_accounts = select_all_accounts(db_engine)
    log.info(f'known cat {known_accounts}')
    sheet = workbook.active

    output_report.write("The following new accounts have been added:")

    for value in sheet.iter_rows(
        min_row=7, max_row=999,
        min_col=3, max_col=3,
        values_only=True,
    ):
        if value[0] is None:
            continue
        if value[0] in known_accounts:
            continue
        add_new_account(db_engine, value[0])
        output_report.write("   " + str(value[0]) + "\n")


def add_new_account(db_engine, account_name):
    global known_accounts
    sql = f"""
        insert into accounts
        (account_name)
        values ('{account_name}')
    """
    db_engine.execute(sql)
    sql = f"""
        select account_id
        from accounts
        where account_name = '{account_name}'
    """
    results = db_engine.execute(sql)
    account_id = results.fetchone()
    known_accounts[account_name] = account_id
