import os
import sys
from dotenv import load_dotenv
from pathlib import Path
import logging
from logging import config

load_dotenv()

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
