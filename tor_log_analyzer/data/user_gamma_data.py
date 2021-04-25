from typing import Dict, Optional


class UserGammaData():
    def __init__(self, data: Optional[Dict] = None):
        self._data = data if data is not None else {}
    
    def __iter__(self):
        return self._data.__iter__()

    def __getitem__(self, username: str) -> int:
        return self._data[username] if username in self._data else 0

    def __setitem__(self, username: str, gamma: str):
        self._data[username] = gamma

    def to_dict(self) -> Dict:
        return self._data
