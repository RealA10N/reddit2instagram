""" A file that tells pytest to accept the reddit client id and secret as
command line arguments, and generates the `praw.Reddit` instances. """

from functools import lru_cache
import pytest
import praw

OPTION_STRINGS = {
    'client_id': '--reddit-client-id',
    'client_secret': '--reddit-client-secret',
    'user_agent': '--reddit-user-agent',
}


def pytest_addoption(parser):

    info = {
        'action': 'store',
        'help': 'Uses to test functions that relay on the reddit API and PRAW',
        'default': None,
    }

    for option_cli_string in OPTION_STRINGS.values():
        parser.addoption(option_cli_string, **info)


@lru_cache()
def get_reddit_instance(*args, **kwargs):
    return praw.Reddit(*args, **kwargs)


@pytest.fixture
def reddit(request):
    """ Returns a `praw.Reddit` instance from the credentials passed to pytest
    as a command line arguments. If one or more required credentials are
    missing, the test skips. """

    credentials = {
        option: request.config.getoption(option_cli_string)
        for option, option_cli_string in OPTION_STRINGS.items()
    }

    if None in credentials.values():
        pytest.skip("Some reddit credentials aren't provided")

    return get_reddit_instance(**credentials)
