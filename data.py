import praw
from praw.models import Subreddit, Submission
from datetime import datetime
import os
import json


class PullSubreddit:

    _IMAGE_FORMARTS = ["png", "jpeg", "jpg"]

    _MAX_SUBMISSIONS_PER_REQUEST = 100
    _SAVE_PULLED_DATA_FOR_X_SECONDS = 60 * 60 * 24 * 90  # 90 days

    SAVED_DATA_FOLDER = "data"
    SAVED_DATA_NAME = "%displayname%.json"  # txt between '%' will be replaced.

    def __init__(self, subreddit: Subreddit,):
        self._sub = subreddit

        self._data_file_path = self._generate_data_filepath(subreddit)
        self._already_pulled = self._get_data_if_exists()

    def pull_submission(self,
                        save_data=True,
                        clear_old_data=True,
                        # None: don't care. True: Must contain.
                        nsfw: bool = None,
                        selfpost: bool = None,
                        image: bool = None,
                        ):

        # Make a request for submissions.
        submissions = self._sub.hot(limit=self._MAX_SUBMISSIONS_PER_REQUEST)

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

                if clear_old_data:
                    self.clear_old_data()
                if save_data:
                    self.save_pulled_data()
                return submission

    def save_pulled_data(self):
        """ Save the pulled sumissions data as a json file inside the special
        `data` folder. This data then will be used in the next run of the script.
        """

        # Create the directory if it does not exist yet
        os.makedirs(self.SAVED_DATA_FOLDER, exist_ok=True)

        # Save the json data
        with open(self._data_file_path, mode='w') as data_file:
            json.dump(self._already_pulled, data_file, indent=4)

    def clear_old_data(self):

        # Save current time to compare to saved ones
        now = datetime.now().timestamp()

        # Create a new list, and "throw" the old values (:
        self._already_pulled = [
            data
            for data in self._already_pulled
            if now - data['timestamp'] <= self._SAVE_PULLED_DATA_FOR_X_SECONDS
        ]

    def _mark_pulled(self, submission: Submission):
        data = {
            "id": submission.id,
            "timestamp": datetime.now().timestamp(),
        }

        self._already_pulled.append(data)

    def _check_if_pulled(self, submission: Submission):
        return any(submission.id == data['id'] for data in self._already_pulled)

    def _generate_data_filepath(self, subreddit: Subreddit):
        """ Generate the path to the data file of the subreddit. """

        filename = self.SAVED_DATA_NAME.replace(
            "%displayname%", subreddit.display_name)
        return os.path.join(self.SAVED_DATA_FOLDER, filename)

    def _get_data_if_exists(self,):
        """ If data already exists, loads and returns it.
        Otherwise, returns an empty list. """

        if os.path.exists(self._data_file_path):
            with open(self._data_file_path) as data_file:
                return json.load(data_file)

        return list()
