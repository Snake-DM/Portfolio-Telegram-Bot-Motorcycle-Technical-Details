from loguru import logger
import os


log_dir = os.path.dirname(os.path.abspath(__file__))
logger.add(os.path.join(log_dir, '{time}_log.log'), level="DEBUG")
