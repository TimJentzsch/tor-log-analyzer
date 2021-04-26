from typing import Dict, Optional


class PostTypeData():
    def __init__(self, data: Optional[Dict] = None):
        self._data = data if data is not None else {}
    
    def __iter__(self):
        return self._data.__iter__()

    def __getitem__(self, post_type: str) -> int:
        return self._data[post_type] if post_type in self._data else 0

    def __setitem__(self, post_type: str, count: str):
        self._data[post_type] = count
    
    def __len__(self):
        return len(self._data)

    def to_dict(self) -> Dict:
        return self._data
