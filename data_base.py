import psycopg2
from psycopg2.extras import RealDictCursor


def get_connection(db):
    connection = psycopg2.connect(db)
    connection.autocommit = True
    return connection


def insert_to_db(connection, category_codename, amount, table='expenses'):
    with connection.cursor() as cursor:
        cursor.execute(
            f"INSERT INTO {table} (category_codename, amount, created_at)\
            VALUES ('{category_codename}', {amount}, NOW());",
        )


def get_category_name(connection, category_codename):
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT name\
            FROM categories\
            WHERE categories.codename='{category_codename}';",
        )
        return cursor.fetchone()[0]


def get_total_expenses_by_categories(connection, table='expenses'):
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT SUM(amount) as totals, categories.name\
            FROM {table} LEFT JOIN categories\
            ON {table}.category_codename=categories.codename\
            GROUP BY categories.name;",
        )
        return cursor.fetchall()


def delete_last_added_expense(connection, table='expenses'):
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            f"SELECT id, amount, categories.name as name\
            FROM {table} LEFT JOIN categories\
            ON {table}.category_codename=categories.codename\
            GROUP BY id, name\
            ORDER BY id desc LIMIT 1;",
        )
        last_expense = cursor.fetchone()
        cursor.execute(f"DELETE FROM expenses WHERE id='{last_expense['id']}'")
        return last_expense
