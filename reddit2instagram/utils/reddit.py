import typing
from io import BytesIO
import requests

from praw.models import Submission
from PIL import Image, UnidentifiedImageError


class SubmissionUtils:
    """ A collection of functions that extract and display information about
    a Reddit submission. """

    @staticmethod
    def links_to_image(submission: Submission) -> bool:
        """ Returns `True` if the submission contains an image. """

        if submission.is_self:
            # If a text post, obviously doesn't contain an image.
            return False

        # Requesting the headers of the link that the submission links to,
        # to check if its an image.

        response = requests.head(submission.url)
        content_type = response.headers.get('content-type')

        return (
            content_type and
            'image' in content_type and
            'gif' not in content_type
        )

    @staticmethod
    def get_image(submission: Submission) -> typing.Optional[Image.Image]:
        """ Downloads the image that the given submission contains, and loads
        it into a Pillow Image instance. If the post doesn't contain an image
        or the image fails to load, returns `None`. """

        if submission.is_self:
            # If it is a text post,
            # there is no image to load and returns `None`.
            return None

        # Downloading the image and checking if download went successfully
        response = requests.get(submission.url)
        if response.status_code != 200:
            return None

        try:
            return Image.open(BytesIO(response.content))

        except UnidentifiedImageError:
            # If image cannot be loaded - It's probably not an image.
            return None
