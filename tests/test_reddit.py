import pytest
import praw

from reddit2instagram.utils import SubmissionUtils


@pytest.mark.parametrize(
    'image_submission_id', (
        'nff5zj',   # .png image (transparent)
        'nfjajc',   # .jpg image
        'nfyahs',   # .gif image (not animated)
        'nfygeo',   # .gif image (animated)
    )
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

    def test_links_to_image(self, reddit_client_id, reddit_client_secret,
                            reddit_user_agent, image_submission_id):
        reddit = self._get_reddit_instance(
            reddit_client_id, reddit_client_secret, reddit_user_agent)

        submission = reddit.submission(id=image_submission_id)
        if not SubmissionUtils.links_to_image(submission):
            pytest.fail(
                f"Submission with ID '{image_submission_id}' contains an image, "
                + "but the image isn't detected."
            )
