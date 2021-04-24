from time import sleep

import praw
from praw.models.reddit.submission import Submission
from praw.models.reddit.comment import Comment

from tor_log_analyzer.config import Config
from tor_log_analyzer.reddit import __user_agent__


class RedditAPI():
    def __init__(self, config: Config):
        self._reddit = praw.Reddit(
            client_id=config.auth.client_id,
            client_secret=config.auth.client_secret,
            user_agent=__user_agent__,
        )

    def get_tor_submission(self, submission_full_name: str) -> Submission:
        submission_id = submission_full_name[3:]
        return self._reddit.submission(id=submission_id)

    def get_target_submission(self, submission_full_name: str) -> Submission:
        tor_submission = self.get_tor_submission(submission_full_name)
        return self._reddit.submission(url=tor_submission.url)

    def get_transcription(self, submission_full_name: str, username: str) -> Comment:
        target_submission = self.get_target_submission(submission_full_name)
        comments = target_submission.comments
        comment_len = len(comments)

        while True:
            comment_list = comments.list()
            for comment in comment_list:
                if isinstance(comment, Comment) and comment.author == username:
                    return comment

            comments.replace_more()

            if len(comments) == comment_len:
                break

            comment_len = len(comments)
            sleep(1)

        return None
