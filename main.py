import logging
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
import random
from sql_funct import add_anek, get_anek_random, get_named_anek
from datetime import datetime
import sys

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = '5394892147:AAFSEgwGahLiIgJsJUbv7MyS7qxPQ5WMfWE'
reply_keyboard = [['/start', '/anekdot'],
                  ['/get_anekdot_random', '/get_anekdot_name']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def anek(update, context):
    update.message.reply_text('Отправляй')
    return 1


def response(update, context):
    add_anek(update.message.text)
    spis = ['Прекрасно',
            'Хммммммммммммммммммммммммммммммммммммммммммм....',
            'Ну такое', 'Хороший анекдот', 'Действительно', 'Неплохо']
    update.message.reply_text(random.choice(spis))
    return ConversationHandler.END


def start(update, context):
    update.message.reply_text('Это бот с базой данных анекдотов - вы можете сами её пополнять, отправляя боту анекдоты.'
                              'Вы конечно можете отправлять суда всякую хрень, но это будет неудобно и вам,'
                              ' когда вы будете запрашивать случайные анекдоты. Так что соблюдаем приличие.',
                              reply_markup=markup)


def stop(update, context):
    update.message.reply_text('Ну не хочешь, как хочешь')
    return ConversationHandler.END


def get_anek_rand(update, context):
    update.message.reply_text(get_anek_random())


def anek_theme(update, context):
    update.message.reply_text('Введитe тему анекдота')
    return 1


def get_name_anek(update, context):
    an = get_named_anek(update.message.text)
    for i in an:
        update.message.reply_text(i)
    return ConversationHandler.END


def text(update, context):
    add_anek(update.message.text)
    spis = ['Прекрасно',
            'Хммммммммммммммммммммммммммммммммммммммммммм....',
            'Ну такое', 'Хороший анекдот', 'Действительно', 'Неплохо']
    update.message.reply_text(random.choice(spis))


updater = Updater(TOKEN)
dp = updater.dispatcher
conv_handler1 = ConversationHandler(
    entry_points=[CommandHandler('anekdot', anek)],
    states={
        1: [MessageHandler(Filters.text & ~Filters.command, response)]
    },
    fallbacks=[CommandHandler('stop', stop)]
)
conv_handler2 = ConversationHandler(
    entry_points=[CommandHandler('get_anekdot_name', anek_theme)],
    states={
        1: [MessageHandler(Filters.text & ~Filters.command, get_name_anek)]
    },
    fallbacks=[CommandHandler('stop', stop)]
)
dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('get_anekdot_random', get_anek_rand))
text_handler = MessageHandler(Filters.text
                              & ~Filters.command, text)
dp.add_handler(conv_handler1)
dp.add_handler(conv_handler2)
dp.add_handler(text_handler)
updater.start_polling()
updater.idle()
