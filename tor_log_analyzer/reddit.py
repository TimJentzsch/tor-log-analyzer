import praw

from tor_log_analyzer import __project_id__, __reddit_author__, __version__, __platform__
from tor_log_analyzer.config import Config

USER_AGENT = f"{__platform__}:{__project_id__}:v{__version__} (by u/{__reddit_author__}"


reddit: praw.Reddit

class RedditAPI():
    def __init__(self, config: Config):
        _reddit = praw.Reddit(
            client_id=config.auth.client_id,
            client_secret=config.auth.client_secret,
            user_agent=USER_AGENT,
        )
