from typing import Dict

from tor_log_analyzer.util import clean_dict


class ColorConfig:
    def __init__(self, primary: str, secondary: str, background: str, text: str, line: str):
        self._primary = primary
        self._secondary = secondary
        self._background = background
        self._text = text
        self._line = line

    @property
    def primary(self) -> str:
        return self._primary

    @property
    def secondary(self) -> str:
        return self._secondary

    @property
    def background(self) -> str:
        return self._background

    @property
    def text(self) -> str:
        return self._text

    @property
    def line(self) -> str:
        return self._line

    def to_dict(self) -> Dict:
        return {
            "primary": self.primary,
            "secondary": self.secondary,
            "background": self.background,
            "text": self.text,
            "line": self.line,
        }


DEFAULT_COLORS = ColorConfig(
    primary="#80cbc4",
    secondary="#438078",
    background="#232323",
    text="#fff",
    line="#484848",
)


def colors_from_dict(config: Dict) -> ColorConfig:
    """
    Creates a color configuration based on the values in a dictionary.
    """
    return ColorConfig(
        primary=config["primary"],
        secondary=config["secondary"],
        background=config["background"],
        text=config["text"],
        line=config["line"],
    )

def colors_from_dict_or_defaults(config: Dict) -> ColorConfig:
    """
    Creates a color configuration based on the values in a dictionary,
    or uses the defaults if some are missing.
    """
    default_dict = DEFAULT_COLORS.to_dict()
    cleaned_config = clean_dict(config)
    return colors_from_dict({**default_dict, **cleaned_config})
