from typing import Dict, Optional
from datetime import datetime
from dateutil import parser

from tor_log_analyzer.util import clean_dict


class EventConfig:
    def __init__(self, name: Optional[str] = None, abrv: Optional[str] = None,
                 start: Optional[datetime] = None, end: Optional[datetime] = None):
        self._name = name
        self._abrv = abrv
        self._start = start
        self._end = end

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def abrv(self) -> Optional[str]:
        return self._abrv

    @property
    def start(self) -> Optional[datetime]:
        return self._start

    @property
    def end(self) -> Optional[str]:
        return self._end

    def to_dict(self) -> Dict:
        return clean_dict({
            "name": self.name,
            "abrv": self.abrv,
            "start": self.start.__str__() if self.start is not None else None,
            "end": self.end.__str__() if self.end is not None else None,
        })


DEFAULT_EVENT = EventConfig()


def event_from_dict(config: Dict) -> EventConfig:
    """
    Creates an event configuration based on the values in a dictionary.
    """
    # Convert times
    start = parser.parse(config["start"]) if "start" in config else None
    end = parser.parse(config["end"]) if "end" in config else None

    return EventConfig(
        name=config["name"],
        abrv=config["abrv"],
        start=start,
        end=end,
    )


def event_from_dict_or_defaults(config: Dict) -> EventConfig:
    """
    Creates an event configuration based on the values in a dictionary,
    or uses the defaults if some are missing.
    """
    default_dict = DEFAULT_EVENT.to_dict()
    cleaned_config = clean_dict(config)
    return event_from_dict({**default_dict, **cleaned_config})
