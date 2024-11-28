import os
import logging
import default_messages
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import expense


TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=default_messages.GREEDING)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=default_messages.HELP)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Проверьте, пожалуйста, команду")


async def add_expenses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        new_expense = await expense.add_expense(update.message.text)
    except TypeError:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Проверьте ввод суммы или катергории",
        )
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=new_expense)


async def total_expenses_by_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = await expense.get_total_expenses_by_categories()
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=text)


async def delete_last_added_expense(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = await expense.delete_last_added_expense()
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=text)


if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)

    total_handler = CommandHandler('total', total_expenses_by_categories)
    application.add_handler(total_handler)

    delete_handler = CommandHandler('del', delete_last_added_expense)
    application.add_handler(delete_handler)

    add_extences_handler = MessageHandler(filters.TEXT, add_expenses)
    application.add_handler(add_extences_handler)

    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    application.run_polling()
