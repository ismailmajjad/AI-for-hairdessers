import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import pytz
from utils.read_params import read_params

def initialize_logger(call_sid):
    params = read_params()
    log_folder = params["paths"]["logs_info"]
    
    # Ensure the logs directory exists
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Create a unique log file name based on the current date and time
    ny_tz = pytz.timezone('America/New_York')
    current_time = datetime.now(ny_tz).strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"call_{current_time}_{call_sid}.log"

    # Set up the log handler
    log_filepath = os.path.join(log_folder, log_filename)
    handler = RotatingFileHandler(log_filepath, maxBytes=100000, backupCount=10)
    handler.setLevel(logging.INFO)

    # Set up the formatter
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]', datefmt='%H:%M:%S')
    handler.setFormatter(formatter)

    # Get the root logger and configure it
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Remove all old handlers to prevent duplicate logs
    while logger.hasHandlers():
        logger.removeHandler(logger.handlers[0])

    logger.addHandler(handler)
    return log_filename, current_time
