import datetime
import calendar
import logging
import openpyxl

import pandas as pd
from settings import *
from models.create_model_motohours import create_db
from models.motohours.model import Users, Data, Session
from sqlalchemy.sql import func
from telegram import *
from telegram.ext import *

# Connect bot, using TOKEN
updater = Updater(TOKEN, use_context=True)
# Create session
act_session = Session()


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance, True


def select_and_sum_query_db(n: int, tg_id: int):
    look_for_date = datetime.datetime.utcnow() - datetime.timedelta(days=n)
    utc_look_for_date = calendar.timegm(look_for_date.utctimetuple())
    results = act_session \
        .query(func.sum(Data.data)) \
        .filter(
        Data.tg_user_id == tg_id,
        Data.received >= utc_look_for_date) \
        .all()
    result = [item[0] for item in results]
    if result[0] is not None:
        str_result = str(datetime.timedelta(minutes=result[0]))
        act_session.commit()
        return str_result
    else:
        return '0'


def start_message(update: Update, context: CallbackContext):
    buttons = [[KeyboardButton(startButtonText),
                KeyboardButton(helpButtonText),
                KeyboardButton(stopButtonText)],
               [KeyboardButton(dailyReportButtonText),
                KeyboardButton(weeklyReportButtonText)],
               [KeyboardButton(yearlyReportButtonText)],
               [KeyboardButton(fullReportButtonText)]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=start_message_text,
                             reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))


def help_message(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=help_message_text)


def stop_message(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=stop_message_text,
                             reply_markup=ReplyKeyboardRemove())


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Вибач '%s' це невідома мені команда" % update.message.text)


def unknown_text(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Вибач, я не зрозумів тебе, ти саме це мав на увазі? - '%s'" % update.message.text)


def message_is_digits(update: Update, context: CallbackContext):
    if update.message.text.isdigit():
        tg_id = update.message.from_user.id
        user_firstname = update.message.from_user.first_name
        user_lastname = update.message.from_user.last_name
        add_user, user_flag = get_or_create(act_session, Users,
                                            tg_user_id=tg_id,
                                            user_nickname=user_firstname,
                                            user_lastname=user_lastname)
        if user_flag:
            logger.warning(f'Created record in Users with params\n '
                           f'tg_user_id= {tg_id}, user_nickname= {user_firstname}, user_lastname= {user_lastname}')
        received = datetime.datetime.utcnow()
        utc_received = calendar.timegm(received.utctimetuple())
        add_data = Data(tg_user_id=tg_id, data=int(update.message.text), received=utc_received)
        act_session.add(add_data)
        act_session.commit()
        callback_text = f'Записано до бази: {update.message.text} хвилин'
        context.bot.send_message(chat_id=update.effective_chat.id, text=callback_text)
        logging.info(f'Add row with user: {tg_id}, data: {update.message.text}')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=error_enter_text)


def last_day_report(update: Update, context: CallbackContext):
    result = select_and_sum_query_db(1, update.message.from_user.id)
    logging.info(f'Reported for user: {update.message.from_user.id}, period: last_day_report, data: {result}')
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Сума за останню добу: {result}")


def last_week_report(update: Update, context: CallbackContext):
    result = select_and_sum_query_db(7, update.message.from_user.id)
    logging.info(f'Reported for user: {update.message.from_user.id}, period: last_week_report, data: {result}')
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Сума за останній тиждень: {result}")


def last_year_report(update: Update, context: CallbackContext):
    result = select_and_sum_query_db(365, update.message.from_user.id)
    logging.info(f'Reported for user: {update.message.from_user.id}, period: last_year_report, data: {result}')
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Сума за останній тиждень: {result}")


def get_full_report(update: Update, context: CallbackContext):
    try:
        result = act_session.query(
            Users.user_nickname,
            Users.user_lastname,
            func.sum(Data.data).label('total_minutes')) \
            .join(Data, Users.tg_user_id == Data.tg_user_id) \
            .group_by(Users.tg_user_id) \
            .order_by(func.sum(Data.data).label('total_minutes')) \
            .all()
        df_result = pd.DataFrame(result)
        # create filename and filepath
        time_mark = datetime.datetime.today().strftime("%Y%m%d-%H%M%S")
        filename = 'report_' + time_mark + '.xlsx'
        reports_path = Path.joinpath(cwd, 'reports')
        Path.mkdir(reports_path, parents=True, exist_ok=True)
        filepath = Path.joinpath(reports_path, filename)
        # save file to folder2
        logging.info(f'Full report saved, file: {filepath}')
        df_result.to_excel(filepath)
        context.bot.send_document(chat_id=update.effective_chat.id,
                                  document=open(filepath, 'rb'),
                                  filename=filename)
        logging.info(f'Full report sent for user: {update.message.from_user.id}, file: {filepath}')
    except Exception as e:
        logging.error(f'Error | get_full_report | {e}')


# Filter known commands
updater.dispatcher.add_handler(CommandHandler('start', start_message))
updater.dispatcher.add_handler(CommandHandler('help', help_message))
updater.dispatcher.add_handler(CommandHandler('stop', stop_message))
updater.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), message_is_digits))
updater.dispatcher.add_handler(CommandHandler('last_day_report', last_day_report))
updater.dispatcher.add_handler(CommandHandler('last_week_report', last_week_report))
updater.dispatcher.add_handler(CommandHandler('last_year_report', last_year_report))
updater.dispatcher.add_handler(CommandHandler('get_full_report', get_full_report))
# Filters out unknown commands
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

if __name__ == '__main__':
    db_is_created = os.path.exists(DATABASE_NAME)
    if not db_is_created:
        create_db()
        logging.info(f'Creating Database {DATABASE_NAME}')
    else:
        logging.warning(f'Database is already exists')
    updater.start_polling()
    logging.info(f'Start Motobot')
