#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from typing import Union, List
from uuid import uuid4
from random import randint, randrange
from telegram import Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, dispatcher

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

image_data = [['https://dolgar-pro.ru/wp-content/uploads/2021/03/moskva-scaled.jpg', 'Москва'],
              ['https://i2.wp.com/guruturizma.ru/wp-content/uploads/2020/12/olimpiyskiy-park.jpg?w=1280&ssl=1', 'Сочи'],
              ['https://img-fotki.yandex.ru/get/60881/30348152.20d/0_90bb3_d23fbd71_orig', 'Калининград'],
            ]
city_data = ['Москва', 'Красноярск', 'Ставраполь', 'Сочи', 'Тюмень', 'Тольятти', 'Калининград']


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Привет {user.mention_markdown_v2()}\!',
    )
    

def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    query.answer()
    text = "Ответ неверный D:"
    if (context.user_data.get(1) == None):
        context.user_data[1] = 0
    if int(query.data) == 1:
        text = "Ура-ура"
        context.user_data[1] += 1
    query.edit_message_text(text)


def quiz_command(update: Update, context: CallbackContext) -> None:
    """Generates quiz question and recalculates the score"""
    if (len(context.user_data) == 0):
        context.user_data['was'] = []
    i = 0
    flag = 0
    while context.user_data['was'].count(i) > 0:
        i += 1
        if i == len(image_data):
            flag = 1
            break
    if flag:
        update.message.reply_text('Вопросы кончились :(')
        return
    context.user_data['was'].append(i)
    update.message.reply_photo(image_data[i][0])
    swaped = randint(0, 1)%2
    other_option = randint(0, len(city_data)-1)
    while city_data[other_option] == image_data[i][1]:
        other_option = randint(0, len(city_data)-1)
    keyboard = [
        [
            InlineKeyboardButton(image_data[i][1] if swaped == 0 else city_data[other_option], callback_data=int(swaped^1)),
            InlineKeyboardButton(city_data[other_option] if swaped == 0 else image_data[i][1], callback_data=int(swaped)),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Выберите вариант ответа:', reply_markup=reply_markup)

def stats_command(update: Update, context: CallbackContext) -> None:
    """Shows score of the quiz when command /stats is issued."""
    if (len(context.user_data) == 0):
        context.user_data[1] = 0
    update.message.reply_text('Ваш текущий счет:')
    update.message.reply_text(context.user_data[1])

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5057862462:AAHZOkwA9iW9ZHi0p2jPUx35madCLt8gzJI")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("stats", stats_command))
    dispatcher.add_handler(CommandHandler("quiz", quiz_command))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


main()