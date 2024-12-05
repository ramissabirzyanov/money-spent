from typing import NamedTuple, Optional
import re
import os
import data_base as db


DATABASE_URL = os.getenv('DATABASE_URL')


CATEGORIES = {
    'пр': 'products',
    'ав': 'car',
    'ка': 'cafe',
    'тр': 'transport',
    'др': 'other',
}


MONTHS = {
    1: 'январь',
    2: 'февраль',
    3: 'март',
    4: 'апрель',
    5: 'май',
    6: 'июнь',
    7: 'июль',
    8: 'август',
    9: 'сентябрь',
    10: 'октябрь',
    11: 'ноябрь',
    12: 'декабрь',
}


class Expense(NamedTuple):
    """Структура добавленного в БД новой покупки"""
    id: Optional[int]
    amount: int
    category_name: str


def _parse_text_message(message: str) -> tuple:
    """Парсит сообщение о покупке"""
    amount = re.search(r"\d+", message.lower())[0]
    category = re.search(r"|".join(CATEGORIES.keys()), message.lower())[0]
    category_codename = CATEGORIES.get(category)
    return amount, category_codename


async def add_expense(message: str) -> Expense:
    """Добавляет в БД новую покупку"""
    parsed_message = _parse_text_message(message)
    amount = parsed_message[0]
    category_codename = parsed_message[1]
    conn = await db.get_connection(DATABASE_URL)
    await db.insert_to_db(conn, category_codename, amount)
    category_name = await db.get_category_name(conn, category_codename)
    new_expense = Expense(id=None, amount=amount, category_name=category_name)
    return f"Покупка в категории {new_expense.category_name} на {new_expense.amount}р."


async def get_current_month_expenses() -> str:
    """Вывод расходов по итогам текущего месяца"""
    conn = await db.get_connection(DATABASE_URL)
    current_month, month_expenses = await db.get_expenses_for_current_month_by_category(conn)
    if month_expenses:
        return f"За {MONTHS[current_month]} потречено:\n" + \
            '\n'.join([f"{total}р. в категории {category}" for total, category in month_expenses])
    return f"За {MONTHS[current_month]} расходов нет"


async def delete_last_added_expense():
    """Удаление последней записи о покупки"""
    conn = await db.get_connection(DATABASE_URL)
    last_expense = await db.delete_last_added_expense(conn)
    return f"Удалена покупка на сумму {last_expense['amount']}р. в категории {last_expense['name']}"
