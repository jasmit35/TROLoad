'''
accounts
'''
import logging as log
import modules.jsstdrpt as rpt

known_accounts = {}


def select_all_accounts(connection):
    sql = """
        select account_name, account_id
        from tro.accounts
        order by account_name
    """
    with connection.cursor() as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()
        connection.commit()

    accounts = dict(results)
    log.debug(f'end   get_all_accounts - returns {accounts}')
    return accounts


def get_account_id(account_name):
    try:
        account_id = known_accounts[account_name]
    except KeyError:
        log.debug(f'Account lookup error on "{account_name}"')
        return None
    return account_id


def select_account_id(connection, account_name):
    sql = f"""
        select account_id
        from tro.accounts
        where account_name = '{account_name}'
    """
    with connection.cursor() as cursor:
        cursor.execute(sql)
        account_id = cursor.fetchone()[0]
    return account_id


def add_new_account(connection, account_name):
    global known_accounts
    log.debug(f'begin add_new_account({account_name})')

    sql = "insert into tro.accounts (account_name) values (%s)"
    with connection.cursor() as cursor:
        cursor.execute(sql, (account_name,))

    account_id = select_account_id(connection, account_name)

    known_accounts[account_name] = account_id

    log.debug(f'end   add_new_account - returns {account_id}')
    return account_id


def load_new_accounts_from_workbook(connection, workbook):
    global known_accounts

    known_accounts = select_all_accounts(connection)

    rpt.write("  The following new accounts have been added:\n")

    sheet = workbook.active
    for value in sheet.iter_rows(
        min_row=7, max_row=999,
        min_col=3, max_col=3,
        values_only=True,
    ):
        account_name = value[0]
        if account_name is None:
            continue
        if account_name in known_accounts.values():
            continue
        add_new_account(connection, account_name)
        rpt.write(f"    {account_name}\n")
    log.debug('end   load_new_accounts_from_workbook - returns None')
