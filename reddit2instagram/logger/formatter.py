import typing
import logging
import re

from termcolor import colored


class PrettyFormater(logging.Formatter):
    """ A custom formatter that is used with the logger in the main script. """

    COLOR_EXPRESSION = re.compile(r'\*(.*?)\*')

    COLORS = {
        logging.DEBUG: None,
        logging.INFO: 'cyan',
        logging.WARNING: 'yellow',
        logging.ERROR: 'red',
    }

    MESSAGES = {
        logging.WARNING: 'Warning: ',
        logging.ERROR: 'Error: ',
    }

    def __init__(self,):
        super().__init__()
        self.count = 0

    def _to_colored_message(self, record: logging.LogRecord) -> str:

        def handle(match: re.Match):
            return colored(
                text=match.group(1),
                color=self.COLORS.get(record.levelno),
                attrs=('bold',),
            )

        return re.sub(self.COLOR_EXPRESSION, handle, record.getMessage())

    def _pre_message(self, record: logging.LogRecord) -> str:
        msg = self.MESSAGES.get(record.levelno)

        return colored(
            text=msg,
            color=self.COLORS.get(record.levelno),
            attrs=('bold',)
        ) if msg else ''

    def format(self, record: logging.LogRecord):
        message = self._to_colored_message(record)
        pre_msg = self._pre_message(record)
        newline = '\n' if record.levelno > logging.INFO else ''

        if self.count == 0:
            msg = f'{pre_msg}{message}{newline}'
        else:
            msg = f'{newline}{pre_msg}{message}'

        self.count += 1
        return msg
