import praw
from praw.models import Subreddit, Submission
from datetime import datetime


class PullSubreddit:

    _IMAGE_FORMARTS = ["png", "jpeg", "jpg"]

    _MAX_SUBMISSIONS_PER_REQUEST = 100
    _SAVE_PULLED_DATA_FOR_X_SECONDS = 60 * 60 * 24 * 90  # 90 days

    def __init__(self, subreddit: Subreddit):
        self._sub = subreddit
        self._already_pulled = list()  # empty list

    def pull_submission(self,
                        # None: don't care. True: Must contain.
                        nsfw: bool = None,
                        selfpost: bool = None,
                        image: bool = None,
                        ):

        # Make a request for submissions.
        submissions = self._sub.hot(limit=5, )

        if image:
            # to search for an image you must search for a link posts only!
            selfpost = False

        for submission in submissions:
            submission: Submission

            if nsfw is not None and submission.over_18 ^ nsfw:
                continue

            if selfpost is not None and submission.is_self ^ selfpost:
                continue

            if image is not None:
                is_img = any(f".{cur_format}" in submission.url
                             for cur_format in self._IMAGE_FORMARTS)
                if is_img ^ image:
                    continue

            if not self._check_if_pulled(submission):
                self._mark_pulled(submission)
                return submission

    def _mark_pulled(self, submission):
        data = {
            "id": submission.id,
            "timestamp": datetime.now().timestamp(),
        }

        self._already_pulled.append(data)

    def _clear_old_data(self):

        # Save current time to compare to saved ones
        now = datetime.now().timestamp()

        # Create a new list, and "throw" the old values (:
        self._already_pulled = [
            data
            for data in self._already_pulled
            if now - data['timestamp'] <= self._SAVE_PULLED_DATA_FOR_X_SECONDS
        ]

    def _check_if_pulled(self, submission):
        return any(submission.id == data['id'] for data in self._already_pulled)
