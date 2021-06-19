from .logger import getPrettyLogger


__version__ = '0.0.1-dev'
__all__ = []


def log_system_info() -> None:
    """ Logs basic information about the `reddit2instagram` package version
    and the running Python version. """

    import sys

    logger = getPrettyLogger(__name__)
    logger.debug(
        'Running *reddit2instagram v%s* with *Python %d.%d.%d*',
        __version__,
        sys.version_info.major,
        sys.version_info.minor,
        sys.version_info.micro,
    )


log_system_info()
