import pytest
import praw
from PIL import Image

from reddit2instagram.utils import SubmissionUtils

IMAGE_SUBMISSION_IDS = (
    'nff5zj',   # .png image (transparent)
    'nfjajc',   # .jpg image
    'nfyahs',   # .gif image (not animated)
    'nfygeo',   # .gif image (animated)
    'ni3u2e',   # .png image (hosted on Imgur)
)

NOT_IMAGE_SUBMISSION_IDS = (
    'nfysvm',    # text only
)


class TestRedditUtils:

    @pytest.mark.parametrize('image_submission_id', IMAGE_SUBMISSION_IDS)
    def test_submission_links_to_image(self, reddit, image_submission_id):

        submission = reddit.submission(id=image_submission_id)
        if not SubmissionUtils.links_to_image(submission):
            pytest.fail(
                f"Submission with ID '{image_submission_id}' contains an image, "
                + "but the image isn't detected."
            )

    @pytest.mark.parametrize('image_submission_id', IMAGE_SUBMISSION_IDS)
    def test_get_image_from_submission(self, reddit, image_submission_id):

        submission = reddit.submission(id=image_submission_id)
        img = SubmissionUtils.get_image(submission)

        assert isinstance(img, Image.Image)
        assert img.width > 0
        assert img.height > 0

    @pytest.mark.parametrize('no_image_submission_id', NOT_IMAGE_SUBMISSION_IDS)
    def test_get_image_from_submission_fails(self, reddit, no_image_submission_id):

        submission = reddit.submission(id=no_image_submission_id)
        img = SubmissionUtils.get_image(submission)
        assert img is None
