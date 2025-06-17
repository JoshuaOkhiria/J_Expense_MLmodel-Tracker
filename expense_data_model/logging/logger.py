import os
import logging
from datetime import datetime


# defining file name
LOG_FILE = f"{datetime.now().strftime('%m_%d_%y_%H_%M_%S')}.log"
# defining file path
log_path = os.path.join(os.getcwd(),'logs', LOG_FILE)
# creating firectory for defined file path
os.makedirs(log_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(log_path, LOG_FILE)

# writing logging code - determines how logged details should appear
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
