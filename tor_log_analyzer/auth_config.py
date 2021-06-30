from typing import Dict, Optional


class AuthConfig:
    def __init__(self, reddit_id: Optional[str], reddit_secret: Optional[str],
    blossom_email: Optional[str], blossom_password: Optional[str], blossom_api_key: Optional[str]):
        self._reddit_id = reddit_id
        self._reddit_secret = reddit_secret
        self._blossom_email = blossom_email
        self._blossom_password = blossom_password
        self._blossom_api_key = blossom_api_key

    @property
    def reddit_id(self) -> Optional[str]:
        return self._reddit_id

    @property
    def reddit_secret(self) -> Optional[str]:
        return self._reddit_secret

    @property
    def blossom_email(self) -> Optional[str]:
        return self._blossom_email

    @property
    def blossom_password(self) -> Optional[str]:
        return self._blossom_password

    @property
    def blossom_api_key(self) -> Optional[str]:
        return self._blossom_api_key

    def to_dict(self) -> Dict:
        return {
            "reddit-id": self.reddit_id,
            "reddit-secret": self.reddit_secret,
            "blossom-email": self.blossom_email,
            "blossom-password": self._blossom_password,
            "blossom-api-key": self.blossom_api_key,
        }


DEFAULT_AUTH = AuthConfig(
    reddit_id=None,
    reddit_secret=None,
    blossom_email=None,
    blossom_password=None,
    blossom_api_key=None
)


def auth_from_dict(config: Dict) -> AuthConfig:
    """
    Creates a color configuration based on the values in a dictionary.
    """
    return AuthConfig(
        reddit_id=config["reddit-id"],
        reddit_secret=config["reddit-secret"],
        blossom_email=config["blossom-email"],
        blossom_password=config["blossom-password"],
        blossom_api_key=config["blossom-api-key"],
    )
