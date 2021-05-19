import pytest
import praw
from PIL import Image

from reddit2instagram.utils import SubmissionUtils

IMAGE_SUBMISSION_IDS = (
    'nff5zj',   # .png image (transparent)
    'nfjajc',   # .jpg image
    'nfyahs',   # .gif image (not animated)
    'nfygeo',   # .gif image (animated)
)

NOT_IMAGE_SUBMISSION_IDS = (
    'nfysvm',    # text only
)


class TestRedditUtils:

    reddit_instances = dict()

    def _get_reddit_instance(self, client_id, client_secret, user_agent) -> praw.Reddit:
        if None in (client_id, client_secret):
            pytest.skip("Reddit API credentails aren't provided")

        else:
            key = (client_id, client_secret, user_agent)

            if key not in self.reddit_instances:
                self.reddit_instances[key] = praw.Reddit(
                    client_id=client_id,
                    client_secret=client_secret,
                    user_agent=user_agent
                )

            return self.reddit_instances[key]

    @pytest.mark.parametrize('image_submission_id', IMAGE_SUBMISSION_IDS)
    def test_submission_links_to_image(self, reddit_client_id, reddit_client_secret,
                                       reddit_user_agent, image_submission_id):
        reddit = self._get_reddit_instance(
            reddit_client_id, reddit_client_secret, reddit_user_agent)

        submission = reddit.submission(id=image_submission_id)
        if not SubmissionUtils.links_to_image(submission):
            pytest.fail(
                f"Submission with ID '{image_submission_id}' contains an image, "
                + "but the image isn't detected."
            )

    @pytest.mark.parametrize('image_submission_id', IMAGE_SUBMISSION_IDS)
    def test_get_image_from_submission(self, reddit_client_id, reddit_client_secret,
                                       reddit_user_agent, image_submission_id):
        reddit = self._get_reddit_instance(
            reddit_client_id, reddit_client_secret, reddit_user_agent)

        submission = reddit.submission(id=image_submission_id)
        img = SubmissionUtils.get_image(submission)

        assert isinstance(img, Image.Image)
        assert img.width > 0
        assert img.height > 0

    @pytest.mark.parametrize('no_image_submission_id', NOT_IMAGE_SUBMISSION_IDS)
    def test_get_image_from_submission_fails(
            self, reddit_client_id, reddit_client_secret,
            reddit_user_agent, no_image_submission_id):
        reddit = self._get_reddit_instance(
            reddit_client_id, reddit_client_secret, reddit_user_agent)

        submission = reddit.submission(id=no_image_submission_id)
        img = SubmissionUtils.get_image(submission)
        assert img is None
