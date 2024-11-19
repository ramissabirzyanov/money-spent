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


def add_expense(message: str) -> Expense:
    """Добавляет в БД новую покупку"""
    parsed_message = _parse_text_message(message)
    amount = parsed_message[0]
    category_codename = parsed_message[1]
    conn = db.get_connection(DATABASE_URL)
    db.insert_to_db(conn, category_codename, amount)
    category_name = db.get_category_name(conn, category_codename)
    new_expense = Expense(id=None, amount=amount, category_name=category_name)
    return f"Покупка в категории {new_expense.category_name} на {new_expense.amount}р."


def get_total_expenses_by_categories() -> str:
    """Подсчет суммы расходов в категории"""
    conn = db.get_connection(DATABASE_URL)
    result = db.get_total_expenses_by_categories(conn)
    return '\n'.join([f"потрачено {total}р. в категории {category}" for total, category in result])


def delete_last_added_expense():
    """Удаление последней записи о покупки"""
    conn = db.get_connection(DATABASE_URL)
    last_expense = db.delete_last_added_expense(conn)
    return f"Удалена покупка на сумму {last_expense['amount']}р. в категории {last_expense['name']}"
