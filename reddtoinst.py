from instabot import Bot as Instabot
import requests
from io import BytesIO
import os
import json
import praw
from typing import Union, List
from praw.models import Subreddit, Submission, Comment
from PIL import Image, ImageFont
from img import Post, Title, TitleCollection
from data import PullSubreddit


class RedditToInstagram:

    CONFIG_FILE_PATH = "config.json"

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

    def pull_submission(self) -> Submission:
        """ Get submission from reddit """
        return self._puller.pull_submission(
            image=True,
            nsfw=self._config["reddit"]["nsfw"]
        )

    def submission_to_img(self, submission: Submission):
        # Convert submission to instagram post
        img = self.image_from_submission(submission)
        post = Post(img)

        return post.generate(titles=self.generate_titles(submission),
                             font=self._font,
                             **self._config["design"]["generate-config"])


class CommentStructure:

    def __init__(self, file_path: str):
        with open(file_path, 'r', encoding='utf8') as f:
            self.__raw = json.load(f)

        if not isinstance(self.__raw, list):
            raise TypeError(
                "Comment structure file must be a list of dictioneris.")

    def reply(self, submission: Submission) -> None:
        return self.__reply(submission, self.__raw)

    def __reply(self,
                sub_or_comm: Union[Submission, Comment],
                structure: List,
                ) -> None:

        for reply in structure:

            if "content" in reply:
                content = self.__convert_content(reply["content"])
                reply_of_reply = sub_or_comm.reply(content)

                if "replies" in reply:
                    for reply_structure in reply["replies"]:
                        self.__reply(reply_of_reply, reply_structure)

    @staticmethod
    def __convert_content(content: str):

        if isinstance(content, str):
            return content

        elif isinstance(content, list):
            return '\n'.join(content)

        else:
            raise ValueError("Content must be a string or a list of strings.")


def main():

    TEMP_FILE_PATH = "tempimg.jpg"

    bot = RedditToInstagram()
    submission = bot.pull_submission()
    image = bot.submission_to_img(submission)

    # Save image temporarily
    image.save(TEMP_FILE_PATH)

    if bot._instabot is None:
        bot.load_instagram()

    # Upload the image to instagram
    bot._instabot.upload_photo(
        TEMP_FILE_PATH,
        caption=submission.title,
        options={"rename": False}
    )

    # Delete temp image
    os.remove(TEMP_FILE_PATH)

    comments = CommentStructure("comments.json")
    comments.reply(submission)


if __name__ == "__main__":
    main()
