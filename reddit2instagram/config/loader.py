import typing
import logging
import os

from functools import cached_property

import praw
from prawcore.exceptions import ResponseException, OAuthException

from validit import ValidateFromYAML, Template, TemplateDict, TemplateList, Optional

from reddit2instagram.exceptions import (
    ConfigurationNotFoundError,
    ConfigurationLoadError,
    ConfigurationNotMatchingTemplateError,
    RedditConnectionError,
    RedditWrongUserError,
)

# flake8: noqa E701
logger = logging.getLogger(__name__)


template = TemplateDict(
    reddit=TemplateDict(
        login=TemplateDict(
            client=TemplateDict(
                id=Template(str),
                secret=Template(str),
            ),
            user=Optional(TemplateDict(
                username=Template(str),
                password=Template(str),
            )),
            agent=Optional(Template(str), default='reddit2instagram'),
        ),
    ),
)


class Loader:

    def __init__(self, path: str):
        path = os.path.abspath(path)
        name = os.path.basename(path)

        try:
            with open(path, 'tr') as file:
                validator = ValidateFromYAML(template, file, title=name)

        except FileNotFoundError: raise ConfigurationNotFoundError(path)
        except UnicodeDecodeError: raise ConfigurationLoadError(path)

        logger.debug('Loaded configuration file *%s*', path)

        if validator.errors:
            raise ConfigurationNotMatchingTemplateError(validator.errors)

        self._validator = validator

    @property
    def data(self,):
        return self._validator.data

    @cached_property
    def reddit(self,) -> praw.Reddit:
        info = self.data['reddit']['login']

        kwargs = {
            'client_id': info['client']['id'],
            'client_secret': info['client']['secret'],
            'user_agent': info['agent'],
        }

        if info.get('user'):
            kwargs.update({
                'username': info['user']['username'],
                'password': info['user']['password'],
            })

        reddit = praw.Reddit(**kwargs)

        try: reddit.auth.scopes()  # trying make a request with credentials
        except ResponseException: raise RedditConnectionError()
        except OAuthException: raise RedditWrongUserError()

        if reddit.read_only:
            logger.debug('Successfully logged into reddit *(read-only mode)*')

        else:
            logger.debug(
                'Successfully logged into reddit with user *%s*',
                reddit.user.me()
            )
