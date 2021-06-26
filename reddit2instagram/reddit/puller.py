import typing

from time import time
from datetime import timedelta
from dataclasses import dataclass

from praw.models import Subreddit, Submission
from simplejsondb import Database, DatabaseFolder

from reddit2instagram.utils import SubmissionUtils

DontCare = None
OptionalBool = typing.Union[DontCare, bool]


@dataclass(frozen=True)
class SubmissionOptions:
    nsfw: bool = False
    selfpost: OptionalBool = DontCare
    image: OptionalBool = DontCare

    def is_matching(self, submission: Submission) -> bool:
        """ Recives a submission and checks if the submission matches the
        options configured in the current instance. Returns `True` if the
        given submission passes the test, otherwise `False`. """

        tests = {
            'nsfw': (
                self.nsfw,
                submission.over_18 or self.nsfw,
            ),
            'selfpost': (
                not self.image or self.selfpost,
                submission.is_self,
            ),
            'image': (
                self.image,
                SubmissionUtils.links_to_image(submission),
            ),
        }

        return all(
            wanted is DontCare or wanted == actual
            for wanted, actual in tests.values()
        )


class SubmissionPuller:

    def __init__(self, subreddit: Subreddit, folder: str):
        self.subreddit = subreddit

        dbfolder = DatabaseFolder(folder, default_factory=lambda _: dict())
        self.db = dbfolder.database(  # pylint:disable=invalid-name
            self.subreddit.display_name
        )

    def pull(self, options: SubmissionOptions = None) -> Submission:
        options = options or SubmissionOptions()

        for submission in self.subreddit.hot():
            submission: Submission
            print(f'testing submission {submission.id}')
            if options.is_matching(submission) and not self.is_registered(submission):
                return submission

    def is_registered(self, submission: Submission) -> bool:
        return submission.id in self.db.data

    def register(self, submission: Submission) -> None:
        self.db.data[submission.id] = time()

    def clear(self, older_then: typing.Union[timedelta, float]) -> None:
        if isinstance(older_then, timedelta):
            older_then = abs(older_then).total_seconds()

        now = time()

        for key, created in self.db.data.items():
            if now - created > older_then:
                self.db.data.pop(key)
