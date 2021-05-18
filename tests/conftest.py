""" A file that tells pytest to accept the reddit client id and secret as
command line arguments. """

import pytest

OPTION_STRINGS = {
    'id': '--reddit-client-id',
    'secret': '--reddit-client-secret',
    'agent': '--reddit-user-agent',
}


def pytest_addoption(parser):

    info = {
        'action': 'store',
        'help': 'Uses to test functions that relay on the reddit API and PRAW',
        'default': None,
    }

    for key in OPTION_STRINGS:
        parser.addoption(OPTION_STRINGS[key], **info)


@pytest.fixture
def reddit_client_id(request):
    return request.config.getoption(OPTION_STRINGS['id'])


@pytest.fixture
def reddit_client_secret(request):
    return request.config.getoption(OPTION_STRINGS['secret'])


@pytest.fixture
def reddit_user_agent(request):
    return request.config.getoption(OPTION_STRINGS['agent'])
