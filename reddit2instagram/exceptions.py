class Reddit2InstagramException(Exception):
    """ A general exception in the reddit2instagram module. All other exceptions
    in reddit2instagram inherit this exception."""


class InvalidTemplateConfiguration(Reddit2InstagramException, TypeError):
    """ An exception that is raised when a template isn't configured
    correctly. """
