from loguru import logger
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
active_dir = 'log_history'
log_file_path = os.path.join(current_dir, active_dir, '{time}_log.log')
# TODO make max 10 files .log in folder
logger.add(log_file_path,
           level="DEBUG",
           rotation="10 MB",
           retention="7 days")
