import traceback, os, logging
from dotenv import load_dotenv

load_dotenv()
default_logger_directory = os.getenv("DEFAULT_LOGGER_DIRECTORY")
default_logger_filename = os.getenv("DEFAULT_LOGGER_FILENAME")

events_logger_directory = os.getenv("EVENTS_LOGGER_DIRECTORY")
events_logger_filename = os.getenv("EVENTS_LOGGER_FILENAME")

import logging
import os

from dotenv import load_dotenv

load_dotenv()


class Logger:

    @staticmethod
    def __set_logger(
        directory: str,
        filename: str,
        logger_name: str
    ) -> logging.Logger:

        os.makedirs(directory, exist_ok=True)

        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)

        log_path = os.path.join(
            directory,
            filename
        )

        # Evitar agregar handlers repetidos
        if not logger.handlers:

            file_handler = logging.FileHandler(
                log_path,
                encoding="utf-8"
            )

            file_handler.setLevel(logging.DEBUG)

            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s",
                "%Y-%m-%d %H:%M:%S"
            )

            file_handler.setFormatter(formatter)

            logger.addHandler(file_handler)

        return logger
    
    @classmethod
    def add_to_system_log(cls, level, message):

        logger = cls.__set_logger(
            os.getenv("DEFAULT_LOGGER_DIRECTORY"),
            os.getenv("DEFAULT_LOGGER_FILENAME"),
            "system_logger"
        )

        logger.log(
            cls.__get_level(level),
            message
        )

    @classmethod
    def add_to_test_log(cls, level, message):

        logger = cls.__set_logger(
            os.getenv("TEST_LOGGER_DIRECTORY"),
            os.getenv("TEST_LOGGER_FILENAME"),
            "test_logger"
        )

        logger.log(
            cls.__get_level(level),
            message
        )

    @classmethod
    def add_to_events_log(cls, level, message):

        logger = cls.__set_logger(
            os.getenv("EVENTS_LOGGER_DIRECTORY"),
            os.getenv("EVENTS_LOGGER_FILENAME"),
            "events_logger"
        )

        logger.log(
            cls.__get_level(level),
            message
        )

    @staticmethod
    def __get_level(level):

        levels = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warn": logging.WARNING,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL,
        }

        return levels.get(
            level.lower(),
            logging.INFO
        )
