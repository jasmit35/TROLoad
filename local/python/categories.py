'''
categories
'''
import logging as log
# import openpyxl

known_categories = {}


def select_all_categories(db_engine):
    sql = """
        select category_name, category_id
        from categories
        order by category_name
    """
    results = db_engine.execute(sql)
    categories = {}
    for row in results:
        categories[row['category_name']] = row['category_id']

    return categories


def load_new_categories_from_workbook(db_engine, workbook, output_report):
    global known_categories
    #  Load the existing categories
    known_categories = select_all_categories(db_engine)
    log.info(f'known cat {known_categories}')
    sheet = workbook.active

    output_report.write("The following new categrories have been added:")

    for value in sheet.iter_rows(
        min_row=4, max_row=99,
        min_col=7, max_col=7,
        values_only=True,
    ):
        if value[0] is None:
            continue
        if value[0] in known_categories:
            continue
        add_new_category(db_engine, value[0])
        output_report.write("   " + str(value[0]) + "\n")


def add_new_category(db_engine, category_name):
    global known_categories
    sql = f"""
        insert into categories
        (category_name, category_type_fk, category_group_fk)
        values ('{category_name}', 0, 0)
    """
    db_engine.execute(sql)
    sql = f"""
        select category_id
        from categories
        where category_name = '{category_name}'
    """
    results = db_engine.execute(sql)
    category_id = results.fetchone()
    known_categories[category_name] = category_id
