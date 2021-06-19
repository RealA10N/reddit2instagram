import typing
import logging
import sys

import reddit2instagram
from . import PrettyFormater


def setup_logger() -> None:
    """ Setup the logger of the module. Called when the module is imported
    using '__init__.py' """

    logger = logging.getLogger(reddit2instagram.__name__)
    logger.setLevel(logging.DEBUG)

    # The stream handler -> output to console
    stream = logging.StreamHandler()
    stream.setLevel(logging.DEBUG)
    stream.setFormatter(PrettyFormater())
    logger.addHandler(stream)

    # log a 'welcome message'
    log_system_info()


def log_system_info() -> None:
    """ Logs basic information about the `reddit2instagram` package version
    and the running Python version. """

    logger = logging.getLogger(__name__)
    logger.debug(
        'Running *reddit2instagram v%s* with *Python %d.%d.%d*',
        reddit2instagram.__version__,
        sys.version_info.major,
        sys.version_info.minor,
        sys.version_info.micro,
    )
