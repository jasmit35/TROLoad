'''
categories
'''
import logging as log
import modules.jsstdrpt as rpt

known_categories = {}


def select_all_categories(connection):
    log.debug('begin select_all_categories()')

    sql = """
        select category_name, category_id
        from tro.categories
        order by category_name
    """
    with connection.cursor() as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()

    categories = dict(results)
    log.debug(f'end   select_all_categorys - returns {categories}')
    return categories


def get_category_id(category_name):
    global known_categories
    log.debug(f'begin get_category_id({category_name})')
    try:
        category_id = known_categories[category_name]
    except KeyError:
        return 0
    log.debug(f'end   get_category_id - returns {category_id}')
    return category_id


def select_category_id(connection, category_name):
    sql = """
        select category_id
        from tro.categories
        where category_name = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, (category_name,))
        results = cursor.fetchone()
        category_id = results[0]
    return category_id


def add_new_category(connection, category_name):
    global known_categories
    log.debug(f'Begin add_new_category({category_name})')

    sql = """
        insert into tro.categories (category_name, category_type_fk, category_group_fk)
        values (%s, %s, %s)
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, (category_name, 0, 0))

    category_id = select_category_id(connection, category_name)
    known_categories[category_name] = category_id

    log.debug(f'end  add_new_category - returns {category_id}')
    return category_id


def load_new_categories_from_workbook(connection, workbook):
    global known_categories
    #  Load the existing categories
    known_categories = select_all_categories(connection)
    sheet = workbook.active

    rpt.write("\n\n  The following new categrories have been added:\n")

    for value in sheet.iter_rows(
        min_row=5, max_row=999,
        min_col=7, max_col=7,
        values_only=True,
    ):
        if value[0] is None:
            continue
        if value[0] in known_categories:
            continue
        add_new_category(connection, value[0])
        rpt.write(" `   " + str(value[0]) + "\n")
