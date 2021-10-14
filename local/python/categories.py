"""
categories
"""


class CategoriesTable:
    def __init__(self, db_conn) -> None:
        self.db_conn = db_conn
        self.buffered_categories = {}

    def get_id(self, cat_name):
        try:
            category_id = self.buffered_categories[cat_name]
        except KeyError:
            sql = """
                select category_id
                from tro.categories
                where category_name = %s
            """
            with self.db_conn.cursor() as cursor:
                cursor.execute(sql, (cat_name,))
                results = cursor.fetchone()
            category_id = results[0]
            self.buffered_categories[cat_name] = category_id
        return category_id

    def insert_category(self, name):
        sql = """
            insert into tro.categories (category_name, category_type_fk, category_group_fk)
            values (%s, %s, %s)
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(sql, (name, 0, 0))

        category_id = self.get_id(name)
        self.buffered_categories[name] = category_id
        return category_id
