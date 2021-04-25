from datetime import datetime
from typing import Dict


class DoneData:
    def __init__(self, time: datetime, post_id: str, username: str):
        self._time = time
        self._post_id = post_id
        self._username = username

    @property
    def time(self) -> datetime:
        return self._time

    @property
    def timestamp(self) -> str:
        return self.time.__str__()

    @property
    def post_id(self) -> str:
        return self._post_id

    @property
    def username(self) -> str:
        return self._username

    def to_dict(self) -> Dict:
        return {
            'timestamp': self.timestamp,
            'post_id': self.post_id,
            'username': self.username,
        }
