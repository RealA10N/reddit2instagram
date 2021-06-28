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



@dataclass(frozen=True)
class Design(ABC):
    submission: Submission

    @property
    @classmethod
    @abstractmethod
    def info(cls) -> DesignInfo:
        """ A class property that saves information about the design template,
        including the template itself, and the name of the design (as it should
        appear in the configuration file). """

    @abstractmethod
    def generate_from_image(self,
                            img: Image.Image,
                            ) -> Image.Image:
        """ Recives a raw image (as it is posted on reddit), and returns the
        designed image that will be posted onto Instagram.

        This method actually defines the design of the Instagram posts, because
        the image that is returned from this function directly gets uploaded to
        instagram. If the implementation of this function returns `None` instance
        of an `Image` instance, `reddit2instagram` will assume that the designer
        failed to design an image for the given submission, and a different
        submission will be picked instead.

        When implementing this method, use the given image and decorate it. The
        submission instance is provided using `self.submission` if it is needed
        (for example, to give credit to the original redditor that posted the image
        and to add his name as a text on top of the image). """

    @abstractmethod
    def generate_from_selfpost(self,) -> Image.Image:
        """ This method assumes that the submission is a selfpost (no image, only
        text), and generates the final image that will be uploaded to Instagram.

        The text, author and  additional information about the submission can be
        accessed using the `self.submission` property, which contains an
        `praw.modules.Submission` instance.  """

    def __repr__(self):
        return f'Design(name={self.info.name!r}, submission={self.submission.id!r})'
