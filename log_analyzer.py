#!/usr/bin/env python
import json
import yaml
import click

from tor_log_analyzer import __project_name__, __version__, __description__
from tor_log_analyzer.main import analyze_logs
from tor_log_analyzer.util import clean_dict
from tor_log_analyzer.config import Config, config_from_dict_or_defaults


def config_from_options(
        # General
        config_file, input_file, output_dir, top_count,
        no_cache, force_cache,
        # Auth
        auth_client_id, auth_client_secret,
        # Colors
        colors_primary, colors_secondary, colors_tertiary,
        colors_background, colors_text, colors_line,
        # Event
        event_name, event_abrv, event_start, event_end
) -> Config:
    """
    Creates the config from the app parameters.
    """
    base_config = {}

    # Load base config file if specified
    if config_file:
        ext = config_file.split(".")[-1]

        with open(config_file) as f:
            if ext in ["json"]:
                base_config = json.load(f)
            elif ext in ["yml", "yaml"]:
                base_config = yaml.load(f, Loader=yaml.SafeLoader)
            else:
                raise RuntimeError(f"Unsupported file extension '.{ext}'.")

    # Assemble cli parameters

    # Authentification
    auth_config_dict = clean_dict({
        "client-id": auth_client_id,
        "client-secret": auth_client_secret,
    })

    merged_auth_config_dict = {
        **base_config["auth"], **auth_config_dict} if "auth" in base_config else auth_config_dict

    # Colors
    color_config_dict = clean_dict({
        "primary": colors_primary,
        "secondary": colors_secondary,
        "tertiary": colors_tertiary,
        "background": colors_background,
        "text": colors_text,
        "line": colors_line,
    })

    merged_color_config_dict = {
        **base_config["colors"], **color_config_dict} if "colors" in base_config else color_config_dict
    
    # Event
    event_config_dict = clean_dict({
        "name": event_name,
        "abrv": event_abrv,
        "start": event_start,
        "end": event_end,
    })

    merged_event_config_dict = {
        **base_config["event"], **event_config_dict} if "event" in base_config else event_config_dict

    # General stuff
    app_config_dict = clean_dict({
        "input-file": input_file,
        "output-dir": output_dir,
        "top-count": top_count,
        "no-cache": no_cache,
        "force-cache": force_cache,
        "auth": merged_auth_config_dict,
        "colors": merged_color_config_dict,
        "event": merged_event_config_dict
    })

    # Overwrite the base config with the cli parameters
    merged_config_dict = {**base_config, **app_config_dict}

    return config_from_dict_or_defaults(merged_config_dict)


@click.command()
# Meta options
@click.option("--version", is_flag=True, default=False, help="Display the program version.")
@click.option("--about", is_flag=True, default=False, help="Display info about the program.")
# General options
@click.option("-c", "--config-file", "config_file", help="path to a .json, .yml or .yaml config file. Can be used as a template, all other options override this file", type=str)
@click.option("-i", "--input-file", "input_file", help="the path to the input file", type=str)
@click.option("-o", "--output-dir", "output_dir", help="the path to the output folder", type=str)
@click.option("-t", "--top-count", "top_count", help="the number of entires in the top X diagrams", type=int)
@click.option("--no-cache/--cache", "no_cache", default=False, help="disables the cache", type=bool)
@click.option("--force-cache", "force_cache", is_flag=True, default=False, help="forces to use the cache and doesn't pull data from Reddit", type=bool)
# Auth options
@click.option("--auth.client-id", "auth_client_id", help="the client id assigned by reddit", type=str)
@click.option("--auth.client-secret", "auth_client_secret", help="the client secret assigned by reddit", type=str)
# Color options
@click.option("--colors.primary", "colors_primary", help="the primary color to use in the charts", type=str)
@click.option("--colors.secondary", "colors_secondary",  help="the secondary color to use in the charts", type=str)
@click.option("--colors.tertiary", "colors_tertiary",  help="the tertiary color to use in the charts", type=str)
@click.option("--colors.background", "colors_background",  help="the background color to use in the charts", type=str)
@click.option("--colors.text", "colors_text",  help="the text color to use on the background color", type=str)
@click.option("--colors.line", "colors_line",  help="the color to use for the chart lines", type=str)
# Event options
@click.option("--event.name", "event_name", help="the name of the event", type=str)
@click.option("--event.abrv", "event_abrv", help="the abbrevation for the event name", type=str)
@click.option("--event.start", "event_start", help="the start time of the event", type=str)
@click.option("--event.end", "event_end", help="the end time of the event", type=str)
def log_analyzer(
        version=False, about=False,
        config_file=None, input_file=None, output_dir=None, top_count=None,
        no_cache=None, force_cache=None,
        event_name=None, event_abrv=None, event_start=None, event_end=None,
        auth_client_id=None, auth_client_secret=None,
        colors_primary=None, colors_secondary=None, colors_tertiary=None,
        colors_background=None, colors_text=None, colors_line=None
):
    if version or about:
        click.echo(f"{__project_name__}, version v{__version__}\n\n{__description__}")
        return 0

    config = config_from_options(
        # General
        config_file, input_file, output_dir, top_count,
        no_cache, force_cache,
        # Auth
        auth_client_id, auth_client_secret,
        # Colors
        colors_primary, colors_secondary, colors_tertiary,
        colors_background, colors_text, colors_line,
        # Event
        event_name, event_abrv, event_start, event_end,
    )

    analyze_logs(config)


if __name__ == "__main__":
    log_analyzer()
