import typing
import logging
import os

from functools import cached_property

import praw
from praw.models import Subreddit
from prawcore.exceptions import ResponseException, OAuthException

from validit import (
    ValidateFromYAML,
    Template,
    TemplateDict,
    TemplateList,
    Optional,
    Options,
)

from reddit2instagram.exceptions import (
    ConfigurationNotFoundError,
    ConfigurationLoadError,
    ConfigurationNotMatchingTemplateError,
    RedditConnectionError,
    RedditWrongUserError,
)

from reddit2instagram import SubmissionOptions

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
        subreddits=TemplateList(Template(str)),
        nsfw=Optional(Template(bool), default=False),
        only=Optional(Options('images', 'text')),
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
        """ Returns a `praw.Reddit` instance that is generated using the data
        in the loaded configuration file. If something goes wrong (for example,
        if the credentials in the configuration file are wrong), raises an
        `ScriptError`. """

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

        return reddit

    def submission_options(self) -> SubmissionOptions:
        """ Returns a dataclass that describes what submissions should be pulled
        from reddit. The submission option is generated from the data in the
        loaded configuration file. """

        info = self.data['reddit']
        kwargs = {'nsfw': info['nsfw']}

        only = info.get('only')
        if only == 'images':
            kwargs.update({'image': True})
        if only == 'text':
            kwargs.update({'selfpost': True})

        return SubmissionOptions(**kwargs)

    def subreddit(self,) -> Subreddit:
        subreddits = self.data['reddit']['subreddits']
        return self.reddit.subreddit('+'.join(subreddits))
