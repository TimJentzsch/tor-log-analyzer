from typing import Dict, Optional, List
import statistics


class UserCharEntry():
    def __init__(self, char_count_list: List[int] = None):
        self._char_count_list = char_count_list if char_count_list is not None else []

    @property
    def char_count_list(self) -> List[int]:
        return self._char_count_list

    @property
    def total(self) -> int:
        return sum(self.char_count_list)

    @property
    def maximum(self) -> int:
        return max(self.char_count_list)

    @property
    def median(self) -> int:
        return statistics.median_high(self.char_count_list)

    @property
    def mean(self) -> float:
        return statistics.mean(self.char_count_list)

    def __add__(self, other):
        if isinstance(other, UserCharEntry):
            return UserCharEntry(
                self.char_count_list + other.char_count_list
            )
        elif isinstance(other, list):
            return UserCharEntry(
                self.char_count_list + other
            )
        elif isinstance(other, int):
            return UserCharEntry(
                self.char_count_list + [other]
            )
        else:
            raise TypeError(
                "Argument must be a UserCharEntry, a List of integers or an integer.")

    def to_dict(self) -> Dict:
        return {
            "total": self.total,
            "maximum": self.maximum,
            "median": self.median,
            "mean": self.mean,
        }


class UserCharData():
    def __init__(self, data: Optional[Dict] = None):
        self._data = data if data is not None else {}

    def __iter__(self):
        return self._data.__iter__()

    def __getitem__(self, username: str) -> int:
        return self._data[username] if username in self._data else UserCharEntry()

    def __setitem__(self, username: str, char_entry: UserCharEntry):
        self._data[username] = char_entry

    def to_dict(self) -> Dict:
        return dict([(key, self._data[key].to_dict())
                     for key in self._data])
