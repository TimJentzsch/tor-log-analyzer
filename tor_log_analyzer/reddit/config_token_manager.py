from praw.util.token_manager import FileTokenManager

from tor_log_analyzer.config import Config


class ConfigTokenManager(FileTokenManager):
    """Provides a token manager that uses a config file."""

    def __init__(self, config: Config):
        super(config.auth.token_file).__init__()
        self._token_file = config.auth.token_file
