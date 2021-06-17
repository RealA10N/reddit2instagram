import typing

from PIL import ImageColor

from validit import Template
from validit.errors.managers import TemplateCheckRaiseOnError as RaiseOnError
from validit.templates.base import ErrorManager
from validit.containers import BaseContainer
from validit.errors import TemplateCheckError


class TemplateCheckColorError(TemplateCheckError):

    def __init__(self,
                 path: typing.List[str],
                 got: str):
        super().__init__(
            path=path,
            msg=f"Unknown color specifier '{got}'"
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
        try:
            # Validate that the data is a string
            super().validate(container, RaiseOnError())

        except TemplateCheckError as error:
            errors.register_error(error)
            return

        try:
            # Try converting the string into a rgb color
            ImageColor.getrgb(container.data)

        except ValueError:
            # If an error is raised while converting the string to an
            # rgb color, registers an error!
            errors.register_error(
                TemplateCheckColorError(
                    path=container.path,
                    got=container.data
                )
            )
