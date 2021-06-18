import typing
import logging
import re
from time import time

from termcolor import colored

from .utils import Singleton


class SingletonMeta(type):
    """ A metaclass that implements the Singleton design pattern in Python """

    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(
                SingletonMeta, cls).__call__(*args, **kwargs)
        return cls.__instances[cls]


class PrettyFormater(logging.Formatter, metaclass=SingletonMeta):
    """ A custom formatter that is used with the logger in the main script. """

    COLOR_EXPRESSION = re.compile(r'\*(.*?)\*')

    COLORS = {
        logging.DEBUG: None,
        logging.INFO: 'cyan',
        logging.WARNING: 'yellow',
        logging.ERROR: 'red',
    }

    def __init__(self,):
        super().__init__()
        self.start = time()

    def _to_colored_message(self, record: logging.LogRecord) -> str:

        def handle(match: re.Match):
            return colored(
                text=match.group(1),
                color=self.COLORS.get(record.levelno),
                attrs=('bold',),
            )

        return re.sub(self.COLOR_EXPRESSION, handle, record.getMessage())

    def _time_string(self,) -> str:
        elapsed = int(time() - self.start)
        minutes = elapsed // 60
        seconds = elapsed % 60

        return colored(
            f'{minutes:02d}:{seconds:02d}',
            color='white',
            attrs=('bold',),
        )

    def format(self, record: logging.LogRecord):
        message = self._to_colored_message(record)
        time = self._time_string()
        sep = colored('|', color='grey')

        return f"{time} {sep} {message}"
