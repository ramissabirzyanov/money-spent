import asyncpg
from datetime import datetime


async def get_connection(db):
    return await asyncpg.connect(db)


async def insert_to_db(connection, category_codename, amount, table='expenses'):
    async with connection.transaction():
        await connection.execute(
            f"INSERT INTO {table} (category_codename, amount, created_at)\
            VALUES ('{category_codename}', {amount}, NOW());",
        )


async def get_category_name(connection, category_codename):
    async with connection.transaction():
        return await connection.fetchval(
            f"SELECT name\
            FROM categories\
            WHERE categories.codename='{category_codename}';",
        )


async def delete_last_added_expense(connection, table='expenses'):
    async with connection.transaction():
        last_expense = await connection.fetchrow(
            f"SELECT id, amount, categories.name as name\
            FROM {table} LEFT JOIN categories\
            ON {table}.category_codename=categories.codename\
            GROUP BY id, name\
            ORDER BY id desc LIMIT 1;",
        )
        await connection.execute(f"DELETE FROM expenses WHERE id='{last_expense['id']}'")
        return last_expense


async def get_expenses_for_current_month_by_category(connection, table='expenses'):
    month = datetime.now().month
    async with connection.transaction():
        month_expense = await connection.fetchval(
            f"SELECT SUM(amount) from {table}\
            WHERE EXTRACT (MONTH FROM created_at)={month};",
        )

        month_expenses_by_cat = await connection.fetch(
            f"SELECT SUM(amount) as totals, categories.name\
            FROM {table} LEFT JOIN categories\
            ON {table}.category_codename=categories.codename\
            WHERE EXTRACT (MONTH FROM created_at)={month}\
            GROUP BY categories.name;",
        )
        return month, month_expense, month_expenses_by_cat
