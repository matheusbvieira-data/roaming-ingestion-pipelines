"""Módulo de logging com formatação colorida para console e persistência em arquivo."""

import logging
import pathlib
from datetime import datetime
from functools import wraps


class ColorFormatter(logging.Formatter):
    """Formatador de log que adiciona cores apenas para saídas no console."""

    # Cores ANSI
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    blue = "\x1b[34;20m"
    reset = "\x1b[0m"

    fmt = "%(asctime)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + fmt + reset,
        logging.INFO: blue + fmt + reset,
        logging.WARNING: yellow + fmt + reset,
        logging.ERROR: red + fmt + reset,
        logging.CRITICAL: bold_red + fmt + reset,
    }

    def format(self, record):
        """Formata o registro de log com cores ANSI.

        Args:
            record (logging.LogRecord): Registro de log a ser formatado.

        """
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


class Logger:
    """Logger personalizado que pode ser estendido para funcionalidades adicionais."""

    def __init__(self, name: str, level: int = logging.INFO) -> None:
        """Inicializa o Logger personalizado.

        Args:
            name (str): Nome do logger.
            level (int, optional): Nível de logging. Padrão é logging.INFO.

        """
        self.__log_path = pathlib.Path("logs")
        self.__log_path.mkdir(exist_ok=True)
        self.__log_filename = (
            self.__log_path
            / f"log_{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )

        self.__formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        self.__logger = logging.getLogger(
            name if type(name) is str else "default_logger"
        )
        self.__logger.setLevel(level if type(level) is int else logging.INFO)
        self.__console_handler = logging.StreamHandler()
        self.__console_handler.setFormatter(ColorFormatter())
        self.__logger.addHandler(self.__console_handler)

        self.__file_handler = logging.FileHandler(self.__log_filename, encoding="utf-8")
        self.__file_handler.setFormatter(self.__formatter)
        self.__logger.addHandler(self.__file_handler)

    def get_logger(self) -> logging.Logger:
        """Retorna o logger configurado.

        Returns:
            logging.Logger: O logger configurado.

        """
        return self.__logger

    def log_function_call(self, func):
        """_summary_.

        Args:
            func (_type_): _description_

        Raises:
            e: _description_

        Returns:
            _type_: _description_
        """

        @wraps(func)  # Helps with debugging and introspection
        def wrapper(*args, **kwargs):
            # Log function start with arguments
            self.get_logger().info(
                f"Starting function: {func.__name__!r} with args: {args}, kwargs: {kwargs}"
            )
            try:
                result = func(*args, **kwargs)  # Call the original function
                # Log function end with the result
                self.get_logger().info(
                    f"Finished function: {func.__name__!r} with result: {result!r}"
                )
                return result
            except Exception as e:
                # Log any exceptions that occur
                self.get_logger().error(f"Error in function {func.__name__!r}: {e}")
                raise e

        return wrapper
