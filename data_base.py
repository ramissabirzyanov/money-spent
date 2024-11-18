import psycopg2



def get_connection(db):
    connection = psycopg2.connect(db)
    connection.autocommit = True
    return connection


def insert_to_db(connection, category_codename, amount, table='expenses'):
    with connection.cursor() as cursor:
        cursor.execute(f"INSERT INTO {table} (category_codename, amount, created_at)\
                        VALUES ('{category_codename}', {amount}, NOW());")

def get_category_name(connection, category_codename):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT name\
                       FROM categories\
                       WHERE categories.codename='{category_codename}';")
        return cursor.fetchone()[0]
    
def get_total_expenses_by_categories(connection):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT SUM(amount) as totals, categories.name\
                        FROM expenses LEFT JOIN categories\
                        ON expenses.category_codename=categories.codename\
                        GROUP BY categories.name;")
        return cursor.fetchall()
