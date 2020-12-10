from instabot import Bot as Instabot
import requests
from io import BytesIO
import os
import json
import praw
from praw.models import Subreddit, Submission
from PIL import Image, ImageFont
from img import Post, Title, TitleCollection
from data import PullSubreddit


class RedditToInstagram:

    CONFIG_FILE_PATH = "config.json"
    TEMP_FILE_PATH = "tempimg.jpg"

    ICONS_FOLDER = os.path.join("assets", "icons")
    REDDIT_ICON = Image.open(os.path.join(
        ICONS_FOLDER, "reddit.png")).convert("L")
    INSTAGRAM_ICON = Image.open(os.path.join(
        ICONS_FOLDER, "instagram.png")).convert("L")

    def __init__(self):
        try:
            with open(self.CONFIG_FILE_PATH) as config_file:
                self._config = json.load(config_file)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Config file not found.\n{e}")

        reddit = praw.Reddit(**self._config['reddit']['login-info'])
        subreddits = reddit.subreddit(
            "+".join(self._config['reddit']['subreddits']))

        self._puller = PullSubreddit(subreddits)
        self._instabot = None  # load using 'load_instagram method'

        font_path = os.path.join(*self._config['design']['font']['path'])
        self._font = ImageFont.truetype(
            font=font_path, size=self._config['design']['font']['size'])

    def load_instagram(self):
        self._instabot = Instabot()
        self._instabot.login(**self._config['instagram']['login-info'])

    def image_from_submission(self, submission: Submission):
        """ Recives a `praw` reddit submission, and returns a pillow `Image`
        object reprenting the submission. If something goes wrong, will return
        `None`. """

        response = requests.get(submission.url)
        if response.status_code != 200:
            return None
        try:
            return Image.open(BytesIO(response.content))
        except:
            return None

    def submission_to_title(self, submission: Submission):
        """ Recives a reddit submission, and returns a title object that represents
        the submission. """

        return Title(
            icon_mask=self.REDDIT_ICON,
            left_text=f"r/{submission.subreddit.display_name}",
            right_text=f"u/{submission.author.name}"
        )

    def instagram_title(self):
        """ Generate a title representing the instagram account. """

        return Title(
            icon_mask=self.INSTAGRAM_ICON,
            right_text=self._config['instagram']['login-info']['username']
        )

    def generate_titles(self, submission: Submission) -> TitleCollection:
        """ Returns a `TitleCollection` with two titles - one representing the
        instagram account, and the other representing the reddit submission. """

        titles = TitleCollection()
        titles.add(self.submission_to_title(submission))
        titles.add(self.instagram_title())
        return titles

    def pull_submission(self):
        # Get submission from reddit
        submission = self._puller.pull_submission(
            image=True,
            nsfw=self._config["reddit"]["nsfw"]
        )

        submission.upvote()  # Upvote submission (:
        return submission

    def submission_to_img(self, submission: Submission):
        # Convert submission to instagram post
        img = self.image_from_submission(submission)
        post = Post(img)

        return post.generate(titles=self.generate_titles(submission),
                             font=self._font,
                             **self._config["design"]["generate-config"])

    def upload_single_post(self):

        # Generate image to upload
        submission = self.pull_submission()
        image = self.submission_to_img(submission)

        # Save image temporarily
        image.save(self.TEMP_FILE_PATH)

        if self._instabot is None:
            self.load_instagram()

        # Upload the image to instagram
        self._instabot.upload_photo(
            self.TEMP_FILE_PATH,
            caption=submission.title,
            options={"rename": False}
        )

        # Delete temp image
        os.remove(self.TEMP_FILE_PATH)


def main():
    RedditToInstagram().upload_single_post()


if __name__ == "__main__":
    main()
