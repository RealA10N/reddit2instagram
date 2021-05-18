from functools import cache
import pytest
import praw

from reddit2instagram.utils import SubmissionUtils


@pytest.mark.parametrize(
    'image_submission_id', (
        'nff5zj',
        'nfjajc',
    )
)
class TestRedditUtils:

    def _get_reddit_instance(self, client_id, client_secret, user_agent) -> praw.Reddit:
        if None in (client_id, client_secret):
            pytest.skip("Reddit API credentails aren't provided")

        else:
            return self.__generate_reddit_instance(client_id, client_secret, user_agent)

    @cache
    def __generate_reddit_instance(self, client_id, client_secret, user_agent):
        return praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )

    def test_links_to_image(self, reddit_client_id, reddit_client_secret,
                            reddit_user_agent, image_submission_id):
        reddit = self._get_reddit_instance(
            reddit_client_id, reddit_client_secret, reddit_user_agent)

        submission = reddit.submission(id=image_submission_id)
        assert SubmissionUtils.links_to_image(submission)
