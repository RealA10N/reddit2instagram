import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass

from PIL import Image
from praw.models import Submission

from validit import Validate, Template, Optional, TemplateDict
from validit.templates import BaseTemplate


@dataclass(frozen=True)
class DesignInfo:

    # The name of the design,
    # as it should appear in the configuration file.
    name: str

    # The design configuration template.
    # used to validate the data given in the configuration file.
    template: BaseTemplate


class Design(ABC):

    @property
    @classmethod
    @abstractmethod
    def _info(cls) -> DesignInfo:
        """ A class property that saves information about the design template,
        including the template itself, and the name of the design (as it should
        appear in the configuration file). """

    @abstractmethod
    def submission_to_image(self,
                            submission: Submission,
                            ) -> typing.Optional[Image.Image]:
        """ A method that recives a reddit submission and converts it into
        a `PIL` image instance. This method actually defines the design of
        the Instagram posts, because the image that is returned from this
        function directly gets uploaded to instagram.
        If the implementation of this function returns `None` instance of
        an `Image` instance, `reddit2instagram` will assume that the designer
        failed to design an image for the given submission, and a different
        submission will be picked instead. """
