class Reddit2InstagramException(Exception):
    pass


class InvalidTemplateConfiguration(Reddit2InstagramException, TypeError):
    """ An exception that is raised when a template isn't configured
    correctly. """
