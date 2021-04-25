from typing import Dict

from praw.models.reddit.comment import Comment


def extract_components(body: str):
    """
    Extracts the header, content and footer of a transcription comment.
    """
    parts = body.split("---")

    header = parts[0].strip()
    content = "---".join(parts[1:-1]).strip()
    footer = parts[-1].strip()

    return (header, content, footer)


class Transcription():
    def __init__(self, tid: str, subreddit: str, author: str, body: str):
        self._id = tid
        self._subreddit = subreddit
        self._author = author
        self._body = body

        header, content, footer = extract_components(body)
        self._header = header
        self._content = content
        self._footer = footer

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

    @property
    def header(self) -> str:
        return self._header

    @property
    def content(self) -> str:
        return self._content

    @property
    def footer(self) -> str:
        return self._footer

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
