#!/usr/bin/env python
from typing import List, Tuple
import json
from os import makedirs
import cli.app
from dateutil import parser
import matplotlib.pyplot as plt

from tor_log_analyzer.done_info import DoneInfo
from tor_log_analyzer.config import Config, config_from_dict_or_defaults


def done_line_to_dict(line: str) -> DoneInfo:
    tokens = line.split(" ")

    # Extract the timestamp
    raw_timestamp = " ".join(tokens[:3])
    time = parser.parse(raw_timestamp)
    # Extract post id
    post_id = tokens[10]
    # Extract username
    username = tokens[13]

    return DoneInfo(time, post_id, username)


def generate_user_stats(config: Config, dones: List[DoneInfo]):
    user_data = {}

    for done in dones:
        user = done.username
        if user in user_data:
            user_data[user] += 1
        else:
            user_data[user] = 1

    with open(f"{config.cache_dir}/user_gamma.json", "w") as f:
        dumps = json.dumps(user_data, indent=2)
        f.write(dumps + "\n")

    top_count = config.top_count

    # Sort by user gamma
    sorted_data: List[Tuple[str, int]] = [
        (f"u/{username}", user_data[username]) for username in user_data]
    sorted_data.sort(key=lambda e: e[1], reverse=True)
    # Extract the top users
    top_list = sorted_data[:top_count]
    top_list.reverse()

    compressed_data: List[Tuple[str, int]] = top_list

    if len(sorted_data) > top_count:
        # Aggregate the rest of the users that didn't make it in the top to a single entry
        rest: List[Tuple[str, int]] = [
            ("Other", sum([entry[1] for entry in sorted_data[top_count:]]))]
        compressed_data = rest + top_list

    labels = [entry[0] for entry in compressed_data]
    data = [entry[1] for entry in compressed_data]

    colors = [config.colors.primary for _ in range(len(top_list))]

    if len(sorted_data) > top_count:
        colors = [config.colors.secondary] + colors

    plt.barh(labels, data, color=colors)
    plt.ylabel("User")
    plt.xlabel("Transcriptions")
    plt.title(f"Top {top_count} Contributors")

    # Annotate data
    for x, y in zip(data, labels):
        plt.annotate(x,  # label with gamma
                     (x, y),
                     textcoords="offset points",
                     xytext=(3, 0),
                     ha="left",
                     va="center")

    plt.savefig(f"{config.image_dir}/user_gamma.png")
    plt.close()


def generate_history(config: Config, dones: List[DoneInfo]):
    history_data = []

    for i, val in enumerate(dones):
        entry = (val.time, i + 1)
        history_data.append(entry)

    dates = [entry[0] for entry in history_data]
    data = [entry[1] for entry in history_data]

    plt.plot(dates, data, color=config.colors.primary)
    plt.xlabel("Time")
    plt.ylabel("Total Transcriptions")
    plt.title("History")

    plt.savefig(f"{config.image_dir}/history.png")
    plt.close()


def process_lines(config: Config, lines: List[str]):
    # Only consider "done"-ed posts
    done_lines = [
        l for l in lines if "process_done" in l and "Moderator override" not in l]

    with open(f"{config.cache_dir}/done.log", "w") as f:
        f.write("\n".join(done_lines))

    dones = [done_line_to_dict(line) for line in done_lines]

    with open(f"{config.cache_dir}/done.json", "w") as f:
        dumps = json.dumps([done.to_dict() for done in dones], indent=2)
        f.write(dumps + "\n")

    generate_user_stats(config, dones)
    generate_history(config, dones)


def configure_plot_style(config: Config):
    """
    Configures the base style for all plots.
    """
    # General
    plt.rcParams['figure.autolayout'] = True
    plt.rcParams['date.autoformatter.hour'] = "%H:%M"

    colors = config.colors

    # Colors
    plt.rcParams['figure.facecolor'] = colors.background
    plt.rcParams['axes.facecolor'] = colors.background
    plt.rcParams['axes.labelcolor'] = colors.text
    plt.rcParams['axes.edgecolor'] = colors.line
    plt.rcParams['text.color'] = colors.text
    plt.rcParams['xtick.color'] = colors.line
    plt.rcParams['xtick.labelcolor'] = colors.text
    plt.rcParams['ytick.color'] = colors.line
    plt.rcParams['ytick.labelcolor'] = colors.text


def config_from_app(app) -> Config:
    """
    Creates the config from the app parameters.
    """
    params = app.params

    app_config_dict = {
        "input-file": params.input,
        "output-dir": params.output,
        "top-count": params.top,
        "colors": {
            "primary": params.primarycolor,
            "secondary": params.secondarycolor,
            "background": params.backgroundcolor,
            "text": params.textcolor,
            "line": params.linecolor,
        }
    }

    return config_from_dict_or_defaults(app_config_dict)


@cli.app.CommandLineApp
def log_analyzer(app):
    config = config_from_app(app)

    # Create all needed directories
    try:
        makedirs(config.output_dir)
        makedirs(config.cache_dir)
        makedirs(config.image_dir)
    except OSError as _:
        pass

    configure_plot_style(config)

    with open(config.input_file) as f:
        lines = f.read().splitlines()
        process_lines(config, lines)


# Set CLI parameters
log_analyzer.add_param(
    "-i", "--input", help="the path to the input file", default="input/input.log", type=str)
log_analyzer.add_param(
    "-o", "--output", help="the path to the output folder", default="output", type=str)
log_analyzer.add_param(
    "-t", "--top", help="the number of entires in the top X diagrams", default=10, type=int)

log_analyzer.add_param(
    "--primarycolor", help="the primary color to use in the graphs", default="#80cbc4", type=str)
log_analyzer.add_param(
    "--secondarycolor", help="the secondary color to use in the graphs", default="#438078", type=str)
log_analyzer.add_param(
    "--backgroundcolor", help="the background color to use in the graphs", default="#232323", type=str)
log_analyzer.add_param(
    "--textcolor", help="the text color to use on the background color", default="#fff", type=str)
log_analyzer.add_param(
    "--linecolor", help="the text color to use on the background color", default="#484848", type=str)

if __name__ == "__main__":
    log_analyzer.run()
