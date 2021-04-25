from typing import Dict
import re

from praw.models.reddit.comment import Comment

from tor_log_analyzer.util import l_includes


def extract_components(body: str):
    """
    Extracts the header, content and footer of a transcription comment.
    """
    parts = body.split("---")

    header = parts[0].strip()
    content = "---".join(parts[1:-1]).strip()
    footer = parts[-1].strip()

    return (header, content, footer)


def extract_format_and_type(header: str):
    """
    Extracts the format and the type of the transcription header.
    """

    # Extract format and type from header
    pattern = re.compile(r"\*(?P<t_format>[\w ]*[\w]+)\s*Transcription:?\s*(?P<t_type>[\w]+.*)?\*", re.IGNORECASE)
    match = pattern.match(header)
    if match is None:
        return (None, None)
    t_format = match.group("t_format")
    t_type = match.group("t_type")
    if t_type is None:
        t_type = t_format
    if l_includes("GIF", t_type):
        t_format = "GIF"
    
    # Merge common types
    if l_includes("Twitter", t_type):
        t_type = "Twitter"
    if l_includes("Facebook", t_type):
        t_type = "Facebook"
    if l_includes("Tumblr", t_type):
        t_type = "Tumblr"
    if l_includes("Reddit", t_type):
        t_type = "Reddit"
    if l_includes("Picture", t_type) or l_includes("Photo", t_type) or l_includes("Photogra", t_type):
        t_type = "Piture"
    if l_includes("Review", t_type):
        t_type = "Review"
    if l_includes("YouTube", t_type):
        t_type = "YouTube"
    if l_includes("Code", t_type):
        t_type = "Code"
    if l_includes("Chat", t_type) or l_includes("Message", t_type) or l_includes("Discord", t_type) or l_includes("Email", t_type) or l_includes("E-mail", t_type):
        t_type = "Chat"
    if l_includes("Meme", t_type):
        t_type = "Meme"
    if l_includes("Social Media", t_type):
        t_type = "Social Media"
    if l_includes("Image", t_type):
        t_type = "Image"
    if l_includes("Video", t_type):
        t_type = "Video"
    if l_includes("Text", t_type):
        t_type = "Text"

    return (t_format, t_type)


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

        t_format, t_type = extract_format_and_type(header)
        self._t_format = t_format
        self._t_type = t_type

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
    
    @property
    def t_format(self) -> str:
        return self._t_format
    
    @property
    def t_type(self) -> str:
        return self._t_type

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
