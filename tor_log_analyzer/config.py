from typing import Dict
from tor_log_analyzer.util import clean_dict
from tor_log_analyzer.auth_config import AuthConfig, DEFAULT_AUTH, auth_from_dict
from tor_log_analyzer.color_config import ColorConfig, DEFAULT_COLORS, colors_from_dict_or_defaults


class Config:
    def __init__(self, input_file: str, output_dir: str, top_count: int, no_cache: bool, force_cache: bool, auth: AuthConfig, colors: ColorConfig):
        self._input_file = input_file
        self._output_dir = output_dir
        self._top_count = top_count
        self._no_cache = no_cache
        self._force_cache = force_cache
        self._auth = auth
        self._colors = colors

    @property
    def input_file(self) -> str:
        return self._input_file

    @property
    def output_dir(self) -> str:
        return self._output_dir

    @property
    def cache_dir(self) -> str:
        return f"{self.output_dir}/.cache"

    @property
    def image_dir(self) -> str:
        return self.output_dir

    @property
    def top_count(self) -> int:
        return self._top_count
    
    @property
    def no_cache(self) -> bool:
        return self._no_cache

    @property
    def force_cache(self) -> bool:
        return self._force_cache

    @property
    def auth(self) -> AuthConfig:
        return self._auth

    @property
    def colors(self) -> ColorConfig:
        return self._colors

    def to_dict(self) -> Dict:
        return {
            "input-file": self.input_file,
            "output-dir": self.output_dir,
            "top-count": self.top_count,
            "no-cache": self.no_cache,
            "force-cache": self.force_cache,
            "colors": self.colors.to_dict(),
            "auth": self.auth.to_dict(),
        }


DEFAULT_CONFIG = Config(
    input_file='input/input.log',
    output_dir='output',
    top_count=10,
    no_cache=False,
    force_cache=False,
    auth=DEFAULT_AUTH,
    colors=DEFAULT_COLORS,
)


def config_from_dict(config: Dict) -> Config:
    """
    Creates a configuration based on the values in a dictionary.
    """
    return Config(
        input_file=config["input-file"],
        output_dir=config["output-dir"],
        top_count=config["top-count"],
        no_cache=config["no-cache"],
        force_cache=config["force-cache"],
        auth=auth_from_dict(config["auth"]),
        colors=colors_from_dict_or_defaults(config["colors"]),
    )


def config_from_dict_or_defaults(config: Dict) -> Config:
    """
    Creates a configuration based on the values in a dictionary,
    or uses the defaults if some are missing.
    """
    default_dict = DEFAULT_CONFIG.to_dict()
    cleaned_config = clean_dict(config)
    return config_from_dict({**default_dict, **cleaned_config})
