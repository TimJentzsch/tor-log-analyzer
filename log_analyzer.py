#!/usr/bin/env python
import json
import yaml
import traceback
import cli.app

from tor_log_analyzer import __project_name__, __version__, __description__
from tor_log_analyzer.main import analyze_logs
from tor_log_analyzer.util import clean_dict
from tor_log_analyzer.config import Config, config_from_dict_or_defaults


def config_from_app(app) -> Config:
    """
    Creates the config from the app parameters.
    """
    params = app.params

    base_config = {}

    # Load base config file if specified
    if params.config:
        config_path = params.config
        ext = config_path.split(".")[-1]

        with open(config_path) as f:
            if ext in ["json"]:
                base_config = json.load(f)
            elif ext in ["yml", "yaml"]:
                base_config = yaml.load(f, Loader=yaml.SafeLoader)
            else:
                raise RuntimeError(f"Unsupported file extension '.{ext}'.")

    # Assemble cli parameters

    # Authentification
    auth_config_dict = clean_dict({
        "clientID": getattr(params, 'auth.clientID', None),
        "clientSecret": getattr(params, 'auth.clientSecret', None),
    })

    merged_auth_config_dict = {
        **base_config["auth"], **auth_config_dict} if "auth" in base_config else auth_config_dict

    # Colors
    color_config_dict = clean_dict({
        "primary": getattr(params, 'colors.primary', None),
        "secondary": getattr(params, 'colors.secondary', None),
        "background": getattr(params, 'colors.background', None),
        "text": getattr(params, 'colors.text', None),
        "line": getattr(params, 'colors.line', None),
    })

    merged_color_config_dict = {
        **base_config["colors"], **color_config_dict} if "colors" in base_config else color_config_dict

    # General stuff
    app_config_dict = clean_dict({
        "input-file": params.input,
        "output-dir": params.output,
        "top-count": params.top,
        "auth": merged_auth_config_dict,
        "colors": merged_color_config_dict,
    })

    # Overwrite the base config with the cli parameters
    merged_config_dict = {**base_config, **app_config_dict}

    return config_from_dict_or_defaults(merged_config_dict)


@cli.app.CommandLineApp(name=__project_name__, version=__version__, description=__description__)
def log_analyzer(app):
    config = config_from_app(app)
    
    try:
        analyze_logs(config)
    except Exception as e:
        print(f"\n\nERROR: {e}")


# Set CLI parameters
log_analyzer.add_param(
    "-c", "--config", help="path to a .json, .yml or .yaml config file. Can be used as a template, all other options override this file", type=str)
log_analyzer.add_param(
    "-i", "--input", help="the path to the input file", type=str)
log_analyzer.add_param(
    "-o", "--output", help="the path to the output folder", type=str)
log_analyzer.add_param(
    "-t", "--top", help="the number of entires in the top X diagrams", type=int)

log_analyzer.add_param(
    "--auth.clientID", help="the client id assigned by reddit", type=str)
log_analyzer.add_param(
    "--auth.clientSecret", help="the client secret assigned by reddit", type=str)

log_analyzer.add_param(
    "--colors.primary", help="the primary color to use in the charts", type=str)
log_analyzer.add_param(
    "--colors.secondary", help="the secondary color to use in the charts", type=str)
log_analyzer.add_param(
    "--colors.background", help="the background color to use in the charts", type=str)
log_analyzer.add_param(
    "--colors.text", help="the text color to use on the background color", type=str)
log_analyzer.add_param(
    "--colors.line", help="the color to use for the chart lines", type=str)

if __name__ == "__main__":
    try:
        log_analyzer.run()
    except RuntimeError:
        pass
