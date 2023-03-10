import logging
import os
from datetime import datetime

#Create Log File for every time instance
LOG_FILE_NAME = f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.log"

#Create Log File directory path
LOG_FILE_DIR = os.path.join(os.getcwd(),"logs")

#Create Log directory if not available
os.makedirs(LOG_FILE_DIR, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_FILE_DIR,LOG_FILE_NAME)

logging.basicConfig(
    filename = LOG_FILE_PATH,
    level = logging.INFO,
    format = "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s"
)

