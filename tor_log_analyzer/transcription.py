from typing import Dict

from praw.models.reddit.comment import Comment


class Transcription():
    def __init__(self, comment: Comment):
        self._id = comment.id
        self._subreddit = comment.subreddit.display_name
        self._author = comment.author.name
        self._body = comment.body

    @property
    def id(self) -> str:
        return self._id
    
    @property
    def subreddit(self) -> str:
        return self._subreddit

    @property
    def author(self) -> str:
        return self._author

    @property
    def body(self) -> str:
        return self._body

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "subreddit": self.subreddit,
            "author": self.author,
            "body": self.body,
        }
