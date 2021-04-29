from typing import List, Tuple
import json
import matplotlib.pyplot as plt

from tor_log_analyzer.transcription import Transcription
from tor_log_analyzer.config import Config
from tor_log_analyzer.data.user_gamma_data import UserGammaData
from tor_log_analyzer.data.user_char_data import UserCharData
from tor_log_analyzer.data.sub_gamma_data import SubGammaData
from tor_log_analyzer.data.post_type_data import PostTypeData

HBAR_HMARGIN = 0.1
HBAR_VMARGIN = 0.02


def add_watermark(config):
    fig: plt.Figure = plt.gcf()
    _, _, fw, fh = fig.bbox.bounds

    posx, posy = 0.02, 0.02

    tor_text = fig.text(posx, posy, "r/TranscribersOfReddit",
                        color=config.colors.secondary, fontsize="10", va="bottom")
    _, yp, _, hp = tor_text.get_tightbbox(
        plt.gcf().canvas.get_renderer()).bounds
    posy2 = (yp + hp) / fh

    txt = fig.text(posx, posy + posy2, "CtQ",
                   color=config.colors.primary, fontsize="17", va="bottom")
    # Calculate where we stopped typing
    xp, _, wp, _ = txt.get_tightbbox(plt.gcf().canvas.get_renderer()).bounds
    posx2 = (xp + wp) / fw
    # Continue text in other color
    fig.text(posx + posx2, posy + posy2, "Mar 26",
             color=config.colors.text, fontsize="14", va="bottom")


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

    add_watermark(config)

    plt.gca().margins(HBAR_HMARGIN, HBAR_VMARGIN)

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


def generate_history(config: Config, transcriptions: List[Transcription]):
    history_data = []

    if config.start_date is not None:
        history_data.append((config.start_date, 0))

    for i, val in enumerate(transcriptions):
        # Add a "step" for each transcription
        history_data.append((val.time, i))
        history_data.append((val.time, i + 1))

    if config.end_date is not None:
        history_data.append((config.end_date, len(transcriptions)))

    dates = [entry[0] for entry in history_data]
    data = [entry[1] for entry in history_data]

    axes = plt.axes((0.12, 0.2, 0.83, 0.72))
    axes.plot(dates, data, color=config.colors.primary)
    axes.grid()
    plt.xlabel("Time")
    plt.ylabel("Total Transcriptions")
    plt.title("History")

    add_watermark(config)

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

    add_watermark(config)

    plt.gca().margins(HBAR_HMARGIN, HBAR_VMARGIN)

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


def generate_type_stats(config: Config, type_data: PostTypeData):
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

    axes = plt.axes((0.2, 0.2, 0.73, 0.72))
    axes.barh(labels, data, color=colors)
    plt.ylabel("Type")
    plt.xlabel("Transcriptions")
    plt.title(f"Top {top_count} Post Types")

    add_watermark(config)

    plt.gca().margins(HBAR_HMARGIN, HBAR_VMARGIN)

    # Annotate data
    for x, y in zip(data, labels):
        plt.annotate(x,  # label with count
                     (x, y),
                     textcoords="offset points",
                     xytext=(3, 0),
                     ha="left",
                     va="center")

    plt.savefig(f"{config.image_dir}/post_types.png")
    plt.close()


def generate_format_stats(config: Config, transcriptions: List[Transcription]):
    format_data = {}

    for tr in transcriptions:
        t_format = tr.t_format
        if t_format in format_data:
            format_data[t_format] += 1
        else:
            format_data[t_format] = 1

    with open(f"{config.cache_dir}/post_formats.json", "w") as f:
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
    plt.title("Top Post Formats")
    plt.gca().axis('equal')

    add_watermark(config)

    plt.savefig(f"{config.image_dir}/post_formats.png")
    plt.close()


def generate_user_count_length_stats(config: Config, user_gamma_data: UserGammaData, user_char_data: UserCharData):
    counts = []
    medians = []

    for username in user_char_data:
        if username in user_gamma_data:
            counts.append(user_gamma_data[username])
            medians.append(user_char_data[username].median)

    axes = plt.axes((0.12, 0.2, 0.83, 0.72))
    axes.scatter(medians, counts, c=[config.colors.primary])
    plt.ylabel("Transcription Count")
    plt.xlabel("Transcription Length Median (Characters)")
    plt.title("Transcription Length vs. Transcription Count")

    add_watermark(config)

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

    add_watermark(config)

    plt.gca().margins(HBAR_HMARGIN, HBAR_VMARGIN)

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


def generate_general_stats(config: Config, user_gamma_data: UserGammaData, sub_gamma_data: SubGammaData, transcription_data: List[Transcription], post_types: PostTypeData):
    stats = {
        "Participants": len(user_gamma_data),
        "Subreddits": len(sub_gamma_data),
        "Post Types": len(post_types),
        "Transcriptions": len(transcription_data),
        "Words written": sum(tr.words for tr in transcription_data),
        "Characters typed": sum(tr.characters for tr in transcription_data),
    }

    plt.axis('off')

    plt.text(0.5, 0.95, "CtQ in Numbers", horizontalalignment='center',
             verticalalignment='center', fontsize='25', color=config.colors.text)

    for i, key in enumerate(stats):
        height = 0.83 - i * 0.13
        color = config.colors.primary if i % 2 == 0 else config.colors.secondary

        formatted_stat = "{:,}".format(stats[key])
        plt.text(0.5, height, f"{formatted_stat} ", horizontalalignment='right',
                 verticalalignment='center', fontsize='25', color=color)
        plt.text(0.5, height, key, horizontalalignment='left',
                 verticalalignment='center', fontsize='15', color=config.colors.text)

    add_watermark(config)

    plt.savefig(f"{config.image_dir}/general_stats.png")
    plt.close()
