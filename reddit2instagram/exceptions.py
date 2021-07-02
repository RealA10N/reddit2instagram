from validit.errors.managers import TemplateCheckErrorCollection as ErrorCollection
from validit.errors import TemplateCheckError


class Reddit2InstagramException(Exception):
    """ A general exception in the reddit2instagram module. All other exceptions
    in reddit2instagram inherit this exception."""


class ScriptError(Reddit2InstagramException):
    """ Exception that is raised while running one of the reddit2instagram scripts.
    The ScriptError exception should be handeld and logged using the logger. """


class ConfigurationNotFoundError(ScriptError, FileNotFoundError):
    def __init__(self, path: str,):
        super().__init__("Configuration file *%s* doesn't exist", path)


class ConfigurationLoadError(ScriptError, TypeError):
    def __init__(self, path: str,):
        super().__init__('Unable to parse file *%s*', path)


class ConfigurationNotMatchingTemplateError(ScriptError, ValueError):

    def __init__(self, errors: ErrorCollection):

        header = f'Found *{errors.count} error(s)* in the given configuration file:'
        lines = list()

        for num, err in enumerate(errors.errors, start=1):
            err: TemplateCheckError
            path = ''.join(f'[{cur!r}]' for cur in err.path) or 'global'
            lines.append(f'*{num})* Under *{path}*: {err.msg}')

        super().__init__(header, *lines)


class RedditConnectionError(ScriptError, RuntimeError):

    def __init__(self,):
        super().__init__(
            'Failed to connect to the reddit servers.',
            '*Perhaps some of the reddit credentials are wrong?*',
        )


class RedditWrongUserError(ScriptError, ValueError):

    def __init__(self,):
        super().__init__(
            'Failed to authorize the given user with the given client.',
            '*Make sure the client application is associated to the right user.*',
        )
