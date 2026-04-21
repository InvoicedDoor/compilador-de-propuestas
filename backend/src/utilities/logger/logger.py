import traceback, os, logging
from dotenv import load_dotenv

load_dotenv()
defaul_logger_directory = os.getenv("DEFAULT_LOGGER_DIRECTORY")
defaul_logger_filename = os.getenv("DEFAULT_LOGGER_FILENAME")

class Logger():

    def __set_logger(self):
        log_directory = defaul_logger_directory
        log_filename = defaul_logger_filename

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        log_path = os.path.join(log_directory, log_filename)

        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', "%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(formatter)

        if (logger.hasHandlers()):
            logger.handlers.clear()

        logger.addHandler(file_handler)

        return logger
    
    @classmethod
    def add_to_log(cls, level, message):
        try:
            logger = cls.__set_logger(cls)

            if (level == "critical"):
                logger.critical(message)
            elif (level == "debug"):
                logger.debug(message)
            elif (level == "error"):
                logger.error(message)
            elif (level == "info"):
                logger.info()
            elif (level == "warn"):
                logger.warning(message)
        except:
            traceback.format_exc()
