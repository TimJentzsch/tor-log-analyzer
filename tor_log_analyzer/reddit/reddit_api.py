import praw
from praw.models.reddit.submission import Submission
from praw.models.reddit.comment import Comment, CommentForest

from tor_log_analyzer.config import Config
from tor_log_analyzer.reddit import __user_agent__
from tor_log_analyzer.reddit.config_token_manager import ConfigTokenManager


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
