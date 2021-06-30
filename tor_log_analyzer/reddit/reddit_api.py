from time import sleep
from typing import Optional

import praw
from praw.models.reddit.submission import Submission
from praw.models.reddit.comment import Comment
from prawcore.exceptions import Forbidden

from tor_log_analyzer.config import Config
from tor_log_analyzer.reddit import __user_agent__, __tor_link__


class RedditAPI():
    def __init__(self, config: Config):
        self._reddit = praw.Reddit(
            client_id=config.auth.reddit_id,
            client_secret=config.auth.reddit_secret,
            user_agent=__user_agent__,
        )

    def get_tor_submission(self, submission_full_name: str) -> Submission:
        submission_id = submission_full_name[3:]
        return self._reddit.submission(id=submission_id)

    def get_target_submission(self, submission_full_name: str) -> Submission:
        tor_submission = self.get_tor_submission(submission_full_name)
        return self._reddit.submission(url=tor_submission.url)

    def get_transcription(self, submission_full_name: str, username: str) -> Comment:
        try:
            target_submission = self.get_target_submission(submission_full_name)
            comments = target_submission.comments
            comment_len = len(comments)
        except Forbidden:
            return None

        tr_comment: Optional[Comment] = None

        print("Getting transcription...")

        while True:
            # print("List iter")
            for comment in comments:
                # print("Comment iter")
                if isinstance(comment, Comment) and comment.author == username:
                    if __tor_link__ in comment.body and "&#32;" in comment.body:
                        # print(f"Transcription found {comment.id}")
                        if tr_comment is None:
                            # Main transcription found
                            tr_comment = comment
                        else:
                            # Add the continued transcription text to the original one
                            tr_comment.body += comment.body
                        
                        # Continue searching for a continued transcription
                        comments = comment.replies
                        comment_len = 0
                        break
            
            comments.replace_more()

            if len(comments) == comment_len:
                break

            comment_len = len(comments)
            sleep(1)

        return tr_comment
