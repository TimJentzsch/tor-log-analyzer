from typing import List, Tuple
from os import makedirs
import json
from dateutil import parser
import matplotlib.pyplot as plt
import click

from tor_log_analyzer.done_info import DoneInfo
from tor_log_analyzer.transcription import Transcription, transcription_from_comment, transcription_from_dict
from tor_log_analyzer.config import Config
from tor_log_analyzer.reddit.reddit_api import RedditAPI


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
            ("Other Volunteers", sum([entry[1] for entry in sorted_data[top_count:]]))]
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


def fetch_transcriptions(config: Config, dones: List[DoneInfo]) -> List[Transcription]:
    cache = {}
    if not config.no_cache:
        with open(f"{config.cache_dir}/transcriptions.json", encoding='utf8') as f:
            try:
                cache = json.load(f)
            except json.JSONDecodeError:
                cache = {}

    reddit_api = RedditAPI(config)
    transcriptions = {}
    with click.progressbar(dones, label="Fetching transcriptions: ") as pbar:
        for done in pbar:
            # Try to get from cache
            if done.post_id in cache:
                transcriptions[done.post_id] = transcription_from_dict(cache[done.post_id])
            # Get transcription from Reddit
            else:
                transcription_comment = reddit_api.get_transcription(
                    done.post_id, done.username)
                if transcription_comment is None:
                    continue
                transcriptions[done.post_id] = transcription_from_comment(transcription_comment)

            with open(f"{config.cache_dir}/transcriptions.json", "w", encoding='utf8') as f:
                json.dump(dict([(key, transcriptions[key].to_dict()) for key in transcriptions]), f, ensure_ascii=False, indent=2)

    return [transcriptions[key] for key in transcriptions]


def generate_sub_stats(config: Config, transcriptions: List[Transcription]):
    sub_data = {}

    for tr in transcriptions:
        sub = tr.subreddit
        if sub in sub_data:
            sub_data[sub] += 1
        else:
            sub_data[sub] = 1

    with open(f"{config.cache_dir}/sub_gamma.json", "w") as f:
        dumps = json.dumps(sub_data, indent=2)
        f.write(dumps + "\n")

    top_count = config.top_count

    # Sort by sub gamma
    sorted_data: List[Tuple[str, int]] = [
        (f"r/{sub}", sub_data[sub]) for sub in sub_data]
    sorted_data.sort(key=lambda e: e[1], reverse=True)
    # Extract the top subs
    top_list = sorted_data[:top_count]
    top_list.reverse()

    compressed_data: List[Tuple[str, int]] = top_list

    if len(sorted_data) > top_count:
        # Aggregate the rest of the subs that didn't make it in the top to a single entry
        rest: List[Tuple[str, int]] = [
            ("Other Subreddits", sum([entry[1] for entry in sorted_data[top_count:]]))]
        compressed_data = rest + top_list

    labels = [entry[0] for entry in compressed_data]
    data = [entry[1] for entry in compressed_data]

    colors = [config.colors.primary for _ in range(len(top_list))]

    if len(sorted_data) > top_count:
        colors = [config.colors.secondary] + colors

    plt.barh(labels, data, color=colors)
    plt.ylabel("Subreddit")
    plt.xlabel("Transcriptions")
    plt.title(f"Top {top_count} Subreddits")

    # Annotate data
    for x, y in zip(data, labels):
        plt.annotate(x,  # label with gamma
                     (x, y),
                     textcoords="offset points",
                     xytext=(3, 0),
                     ha="left",
                     va="center")

    plt.savefig(f"{config.image_dir}/sub_gamma.png")
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
    transcriptions = fetch_transcriptions(config, dones)
    generate_sub_stats(config, transcriptions)


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


def analyze_logs(config: Config):
    """
    Analyze the logs with the given configuration.
    """
    # Create all needed directories
    try:
        makedirs(config.output_dir)
        makedirs(config.cache_dir)
        makedirs(config.image_dir)
    except OSError as _:
        pass

    configure_plot_style(config)

    # Read the logs and process them
    with open(config.input_file) as f:
        lines = f.read().splitlines()
        process_lines(config, lines)
