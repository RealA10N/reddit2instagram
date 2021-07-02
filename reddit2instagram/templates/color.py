import typing

from PIL import ImageColor

from validit import Template
from validit.containers import BaseContainer
from validit.errors import TemplateCheckError
from validit.errors.managers import (
    TemplateCheckErrorManager as ErrorManager,
    TemplateCheckErrorCollection as ErrorCollection,
)


class TemplateCheckColorError(TemplateCheckError):

    def __init__(self,
                 container: BaseContainer,
                 ) -> None:
        super().__init__(
            container=container,
            msg=f"Unknown color specifier '{container.data}'"
        )


class TemplateColor(Template):
    """ A template that insures given data is a string that represents a color.
    This string can be a color from a predefined list of colors (for example:
    'red', 'black', 'hotpink', etc), or a different representation of a custom
    color (for example a hex representation using '#12abef').
    The validation is using the `ImageColor` module that is provided and used
    by the Python Imaging Library (PIL). """

    def __init__(self,):
        # The color should be represented by a string
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
            return

        try:
            # Try converting the string into a rgb color
            ImageColor.getrgb(container.data)

        except ValueError:
            # If an error is raised while converting the string to an
            # rgb color, registers an error!
            errors.register_error(
                TemplateCheckColorError(
                    container=container,
                )
            )
