import os

from validit import Template
from validit.containers import BaseContainer
from validit.errors import TemplateCheckError
from validit.errors.managers import (
    TemplateCheckErrorManager as ErrorManager,
    TemplateCheckErrorCollection as ErrorCollection,
)


class TemplateCheckPathNotFoundError(TemplateCheckError):

    def __init__(self,
                 container: BaseContainer,
                 ) -> None:
        fullpath = os.path.abspath(container.data)
        super().__init__(
            container=container,
            msg=f"No such file or directory '{fullpath}'",
        )


class TemplatePath(Template):
    """ A template that insures the given data is a string that represents a
    path to a folder or a file that exists. """

    def __init__(self):
        # The path should be represented by a string
        super().__init__(str)

    def validate(self,
                 container: BaseContainer,
                 errors: ErrorManager
                 ) -> None:
        temp_errors = ErrorCollection()
        super().validate(container, temp_errors)

        if temp_errors:
            # If there are errors in the `super` validate method
            temp_errors.dump_errors(errors)

        elif not os.path.exists(container.data):
            # Checking if the path exists
            errors.register_error(
                TemplateCheckPathNotFoundError(container)
            )
