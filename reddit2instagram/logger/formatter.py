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

    def format(self, record: logging.LogRecord) -> str:
        message = self._to_colored_message(record)
        pre_msg = self._pre_message(record)

        lines = (pre_msg + message).splitlines()

        spacing = len(self.MESSAGES.get(record.levelno, ''))
        for i, line in enumerate(lines[1:], start=1):
            lines[i] = (spacing * ' ') + line

        if record.levelno >= logging.WARNING:
            lines.insert(0, '')

        return '\n'.join(lines)
