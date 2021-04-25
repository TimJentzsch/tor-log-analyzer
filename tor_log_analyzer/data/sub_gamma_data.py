from typing import Dict, Optional


class SubGammaData():
    def __init__(self, data: Optional[Dict] = None):
        self._data = data if data is not None else {}
    
    def __iter__(self):
        return self._data.__iter__()

    def __getitem__(self, subreddit: str) -> int:
        return self._data[subreddit] if subreddit in self._data else 0

    def __setitem__(self, subreddit: str, gamma: str):
        self._data[subreddit] = gamma

    def to_dict(self) -> Dict:
        return self._data
