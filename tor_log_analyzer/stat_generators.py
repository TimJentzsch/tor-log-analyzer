from typing import List, Tuple
import json
import matplotlib.pyplot as plt

from tor_log_analyzer.data.done_data import DoneData
from tor_log_analyzer.transcription import Transcription
from tor_log_analyzer.config import Config
from tor_log_analyzer.data.user_gamma_data import UserGammaData
from tor_log_analyzer.data.user_char_data import UserCharData
from tor_log_analyzer.data.sub_gamma_data import SubGammaData


def generate_user_gamma_stats(config: Config, user_gamma_data: UserGammaData):
    top_count = config.top_count

    # Sort by user gamma
    sorted_data: List[Tuple[str, int]] = [
        (f"u/{username}", user_gamma_data[username]) for username in user_gamma_data]
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
    plt.title(f"Top {top_count} Contributors with the Most Transcriptions")

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


def generate_history(config: Config, dones: List[DoneData]):
    history_data = []

    for i, val in enumerate(dones):
        entry = (val.time, i + 1)
        history_data.append(entry)

    dates = [entry[0] for entry in history_data]
    data = [entry[1] for entry in history_data]

    plt.grid()
    plt.plot(dates, data, color=config.colors.primary)
    plt.xlabel("Time")
    plt.ylabel("Total Transcriptions")
    plt.title("History")

    plt.savefig(f"{config.image_dir}/history.png")
    plt.close()


def generate_sub_stats(config: Config, sub_gamma_data: SubGammaData):
    top_count = config.top_count

    # Sort by sub gamma
    sorted_data: List[Tuple[str, int]] = [
        (f"r/{sub}", sub_gamma_data[sub]) for sub in sub_gamma_data]
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
    plt.title(f"Top {top_count} Subreddits with the Most Transcriptions")

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


def generate_type_stats(config: Config, transcriptions: List[Transcription]):
    type_data = {}

    for tr in transcriptions:
        t_type = tr.t_type
        if t_type in type_data:
            type_data[t_type] += 1
        else:
            type_data[t_type] = 1

    with open(f"{config.cache_dir}/types.json", "w") as f:
        dumps = json.dumps(type_data, indent=2)
        f.write(dumps + "\n")

    top_count = config.top_count

    # Sort by types
    sorted_data: List[Tuple[str, int]] = [
        (f"{t_type}", type_data[t_type]) for t_type in type_data]
    sorted_data.sort(key=lambda e: e[1], reverse=True)
    # Extract the top subs
    top_list = sorted_data[:top_count]
    top_list.reverse()

    compressed_data: List[Tuple[str, int]] = top_list

    if len(sorted_data) > top_count:
        # Aggregate the rest of the subs that didn't make it in the top to a single entry
        rest: List[Tuple[str, int]] = [
            ("Other Types", sum([entry[1] for entry in sorted_data[top_count:]]))]
        compressed_data = rest + top_list

    labels = [entry[0] for entry in compressed_data]
    data = [entry[1] for entry in compressed_data]

    colors = [config.colors.primary for _ in range(len(top_list))]

    if len(sorted_data) > top_count:
        colors = [config.colors.secondary] + colors

    plt.barh(labels, data, color=colors)
    plt.ylabel("Type")
    plt.xlabel("Transcriptions")
    plt.title(f"Top {top_count} Types")

    # Annotate data
    for x, y in zip(data, labels):
        plt.annotate(x,  # label with count
                     (x, y),
                     textcoords="offset points",
                     xytext=(3, 0),
                     ha="left",
                     va="center")

    plt.savefig(f"{config.image_dir}/types.png")
    plt.close()


def generate_format_stats(config: Config, transcriptions: List[Transcription]):
    format_data = {}

    for tr in transcriptions:
        t_format = tr.t_format
        if t_format in format_data:
            format_data[t_format] += 1
        else:
            format_data[t_format] = 1

    with open(f"{config.cache_dir}/formats.json", "w") as f:
        dumps = json.dumps(format_data, indent=2)
        f.write(dumps + "\n")

    top_count = config.top_count

    # Sort by types
    sorted_data: List[Tuple[str, int]] = [
        (f"{t_format}", format_data[t_format]) for t_format in format_data]
    sorted_data.sort(key=lambda e: e[1], reverse=True)
    # Extract the top subs
    top_list = sorted_data[:top_count]
    top_list.reverse()

    compressed_data: List[Tuple[str, int]] = top_list

    if len(sorted_data) > top_count:
        # Aggregate the rest of the subs that didn't make it in the top to a single entry
        rest: List[Tuple[str, int]] = [
            ("Other Formats", sum([entry[1] for entry in sorted_data[top_count:]]))]
        compressed_data = rest + top_list

    data = [entry[1] for entry in compressed_data]
    total = sum(data)
    labels = [
        f"{entry[0]}\n{entry[1]} ({round(entry[1] * 100 / total)}%)" for entry in compressed_data]

    colors = [config.colors.primary, config.colors.secondary,
              config.colors.tertiary] * (len(top_list) // 3 + 1)
    colors.reverse()

    if len(sorted_data) > top_count:
        colors = [config.colors.secondary] + colors

    plt.pie(data, labels=labels, colors=colors)
    plt.title(f"Top {top_count} Formats")
    plt.gca().axis('equal')

    plt.savefig(f"{config.image_dir}/formats.png")
    plt.close()


def generate_user_count_length_stats(config: Config, user_gamma_data: UserGammaData, user_char_data: UserCharData):
    counts = []
    medians = []

    for username in user_char_data:
        if username in user_gamma_data:
            counts.append(user_gamma_data[username])
            medians.append(user_char_data[username].median)

    plt.scatter(medians, counts, c=[config.colors.primary])
    plt.ylabel("Transcription Count")
    plt.xlabel("Transcription Length Median (Characters)")
    plt.title("Transcription Length vs. Transcription Count")

    plt.savefig(f"{config.image_dir}/user_count_length.png")
    plt.close()


def generate_user_max_length_stats(config: Config, user_char_data: UserCharData):
    top_count = config.top_count

    # Sort by user gamma
    sorted_data: List[Tuple[str, int]] = [
        (f"u/{username}", user_char_data[username].maximum) for username in user_char_data]
    sorted_data.sort(key=lambda e: e[1], reverse=True)
    # Extract the top users
    top_list = sorted_data[:top_count]
    top_list.reverse()

    compressed_data: List[Tuple[str, int]] = top_list[:top_count]

    labels = [entry[0] for entry in compressed_data]
    data = [entry[1] for entry in compressed_data]

    colors = [config.colors.primary for _ in range(len(top_list))]

    plt.barh(labels, data, color=colors)
    plt.ylabel("User")
    plt.xlabel("Longest Transcription (Characters)")
    plt.title(f"Top {top_count} Contributors with the Longest Transcriptions")

    # Annotate data
    for x, y in zip(data, labels):
        plt.annotate(x,  # label with gamma
                     (x, y),
                     textcoords="offset points",
                     xytext=(3, 0),
                     ha="left",
                     va="center")

    plt.savefig(f"{config.image_dir}/user_max_length.png")
    plt.close()
