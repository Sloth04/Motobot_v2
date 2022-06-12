import os
import sys
from dotenv import load_dotenv
from pathlib import Path
import logging

load_dotenv()

# SECRETS
TOKEN = os.getenv('TOKEN')
DATABASE_NAME = os.getenv('DATABASE_NAME')
cwd = Path.cwd()

# LOGGER
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s',
                              '%m-%d-%Y %H:%M:%S')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler('motobot_logs.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)

# TEXT
startButtonText = '/start'
helpButtonText = '/help'
stopButtonText = '/stop'

dailyReportButtonText = '/last_day_report'
weeklyReportButtonText = '/last_week_report'
yearlyReportButtonText = '/last_year_report'
fullReportButtonText = '/get_full_report'

start_message_text = "Привіт, тебе вітає Мотобот, для опису введіть /help"

help_message_text = "Цей бот створений для того, щоб відстежувати та зберігати час у вашій локальній базі даних." \
               "Усі дані вводити як кількість хвилин, які були витрачені на роботу." \
               "Наприклад для того, щоб ввести годину введіть:" \
               "60" \
               "Бот може видавити звіти кожному учаснику, для того щоб обрати термін звітування скористуйтесь меню." \
               "Можемо починати!)"

stop_message_text = f"Вимикаюсь, щоб почати спочатку введіть {startButtonText}"
