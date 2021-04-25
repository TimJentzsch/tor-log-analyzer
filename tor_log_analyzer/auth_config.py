from typing import Dict, Optional


class AuthConfig:
    def __init__(self, client_id: Optional[str], client_secret: Optional[str]):
        self._client_id = client_id
        self._client_secret = client_secret

    @property
    def client_id(self) -> Optional[str]:
        return self._client_id

    @property
    def client_secret(self) -> Optional[str]:
        return self._client_secret

    def to_dict(self) -> Dict:
        return {
            "client-id": self.client_id,
            "client-secret": self.client_secret,
        }


DEFAULT_AUTH = AuthConfig(
    client_id=None,
    client_secret=None,
)


def auth_from_dict(config: Dict) -> AuthConfig:
    """
    Creates a color configuration based on the values in a dictionary.
    """
    return AuthConfig(
        client_id=config["client-id"],
        client_secret=config["client-secret"]
    )
