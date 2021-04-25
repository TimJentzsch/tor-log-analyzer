from typing import Dict

from praw.models.reddit.comment import Comment


class Transcription():
    def __init__(self, tid: str, subreddit: str, author: str, body: str):
        self._id = tid
        self._subreddit = subreddit
        self._author = author
        self._body = body

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


def transcription_from_dict(transcription: Dict) -> Transcription:
    return Transcription(
        tid=transcription["id"],
        subreddit=transcription["subreddit"],
        author=transcription["author"],
        body=transcription["body"],
    )


def transcription_from_comment(comment: Comment) -> Transcription:
    return Transcription(
        tid=comment.id,
        subreddit=comment.subreddit.display_name,
        author=comment.author.name,
        body=comment.body,
    )
