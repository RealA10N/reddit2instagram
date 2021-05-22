import typing


class TemplateCheckError:
    """ A general object that represents a template check error.
    Although you can create instances of it, it is highly recommended to use
    subclasses of it to better describe the check error. """

    ERROR_TITLE = None

    def __init__(self, path: typing.List[str], msg: str = None):
        self.path = path
        self.msg = msg

    @property
    def path_str(self,) -> str:
        """ A string that represents the path where the template check error
        occurred. """

        sep = '.'
        return sep + sep.join(self.path)

    @property
    def description(self,) -> str:
        """ Generates and returns a string that represents the current template
        check error. """

        msg = str()

        if self.ERROR_TITLE:
            msg += self.ERROR_TITLE + ': '

        msg += self.path_str

        if self.msg:
            msg += ' - ' + self.msg

        return msg


class TemplateCheckMissingDataError(TemplateCheckError):
    """ An object that represents a template check error in which some required
    data is missing. """

    ERROR_TITLE = 'MISSING DATA'

    def __init__(self, path):
        super().__init__(path)


class TemplateCheckInvalidDataError(TemplateCheckError):
    """ An object that represents a template check error in which the expected
    data was found, but it didn't follow the expected format / type. """

    ERROR_TITLE = 'INVALID DATA'

    def __init__(self, path, expected: type, got: type):
        self.expected = expected
        self.got = got

        super().__init__(
            path,
            msg=f"Expected '{self.expected_str}', got '{self.got_str}'",
        )

    @property
    def expected_str(self,) -> str:
        """ A string that represents the expected type """
        return type(self.expected).__name__

    @property
    def got_str(self,) -> str:
        """ A string that represents the given type """
        return type(self.got).__name__
