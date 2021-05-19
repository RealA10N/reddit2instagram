import typing
from io import BytesIO
import requests

from praw.models import Submission, Subreddit
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
        return content_type and content_type.startswith('image')

    @staticmethod
    def get_image(submission: Submission) -> typing.Optional[Image.Image]:
        """ Downloads the image that the given submission contains, and loads
        it into a Pillow Image instance. If the post doesn't contain an image
        or the image fails to load, returns `None`. """

        if not submission.is_self:  # If not a text post
            return SubmissionUtils._image_from_url(submission.url)

    @staticmethod
    def get_subreddit_icon(submission: Submission
                           ) -> typing.Optional[Image.Image]:
        """ Returns the icon of the subreddit that the given submission is
        posted in. If there is no icon for the subreddit, returns None. """

        pic_url = submission.subreddit.community_icon
        if pic_url:
            return SubmissionUtils._image_from_url(pic_url)

    @staticmethod
    def _image_from_url(url: str) -> typing.Optional[Image.Image]:
        """ Downloads the image in the provided url and returns it as a Pillow
        Image instance. If something fails, returns `None`. """

        response = requests.get(url)
        if response is not None and response.status_code == 200:
            try:  # Try loading the image
                return Image.open(BytesIO(response.content))
            except UnidentifiedImageError:  # If image cannot be loaded
                return None
