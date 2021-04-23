from typing import Dict, Optional


class AuthConfig:
    def __init__(self, client_id: str, client_secret: str):
        self._client_id = client_id
        self._client_secret = client_secret

    @property
    def client_id(self) -> str:
        return self._client_id

    @property
    def client_secret(self) -> str:
        return self._client_secret

    def to_dict(self) -> Dict:
        return {
            "clientID": self.client_id,
            "clientSecret": self.client_secret,
        }


def auth_from_dict(config: Dict) -> AuthConfig:
    """
    Creates a color configuration based on the values in a dictionary.
    """
    return AuthConfig(
        client_id=config["clientID"],
        client_secret=config["clientSecret"]
    )
