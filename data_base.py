import asyncpg


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


async def get_total_expenses_by_categories(connection, table='expenses'):
    async with connection.transaction():
        return await connection.fetch(
            f"SELECT SUM(amount) as totals, categories.name\
            FROM {table} LEFT JOIN categories\
            ON {table}.category_codename=categories.codename\
            GROUP BY categories.name;",
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
    
async def get_total_expenses_for_last_month(connection, table='expenses'):
    async with connection.transaction():
        month =  await connection.fetchval(
            f"SELECT EXTRACT (MONTH FROM created_at)\
            FROM {table}\
            ORDER BY id desk LIMIT 1;",
        )
        month_expenses = await connection.fetch(
            f"SELECT SUM(amount) as totals, categories.name\
            FROM {table} LEFT JOIN categories\
            ON {table}.category_codename=categories.codename\
            WHERE EXTRACT (MONTH FROM created_at)={month}\
            GROUP BY categories.name;",
        )
        return month, month_expenses
