import telegram.ext

from settings import *
from models.create_model_motohours import create_db

from telegram import *
from telegram.ext import *

updater = Updater(TOKEN, use_context=True)

startButtonText = '/start'
helpButtonText = '/help'
stopButtonText = '/stop'


def start_message(update: Update, context: CallbackContext):
    buttons = [[KeyboardButton(startButtonText)], [KeyboardButton(helpButtonText)], [KeyboardButton(stopButtonText)]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привіт, тебе вітає Мотобот",
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))


def help_message(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Цей бот може зберігати дані у твою локальну базу даних, тому ти завжди можешь "
                                  "слідкувати за витратою часу")


def stop_message(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Вимикаюсь, щоб почати спочатку введіть {startButtonText}",
                             reply_markup=ReplyKeyboardRemove())


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Вибач '%s' це невідома мені команда" % update.message.text)


def unknown_text(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Вибач, я не зрозумів тебе, ти саме це мав на увазі? - '%s'" % update.message.text)


updater.dispatcher.add_handler(CommandHandler('start', start_message))
updater.dispatcher.add_handler(CommandHandler('help', help_message))
updater.dispatcher.add_handler(CommandHandler('stop', stop_message))

# Filters out unknown commands
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))

# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

if __name__ == '__main__':
    db_is_created = os.path.exists(DATABASE_NAME)
    if not db_is_created:
        create_db()
        logging.debug(f'Creating Database {DATABASE_NAME}')
    else:
        logging.warning(f'Database was already created')
    updater.start_polling()
    logging.info(f'Start Motobot')
