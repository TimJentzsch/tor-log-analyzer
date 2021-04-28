from typing import List
from datetime import timedelta
from dateutil import parser
import json
import click

from tor_log_analyzer.data.sub_gamma_data import SubGammaData
from tor_log_analyzer.data.user_char_data import UserCharData
from tor_log_analyzer.data.user_gamma_data import UserGammaData
from tor_log_analyzer.data.post_type_data import PostTypeData
from tor_log_analyzer.data.done_data import DoneData
from tor_log_analyzer.config import Config
from tor_log_analyzer.transcription import Transcription, transcription_from_comment, transcription_from_dict
from tor_log_analyzer.reddit.reddit_api import RedditAPI


def done_line_to_dict(line: str) -> DoneData:
    tokens = line.split(" ")

    # Extract the timestamp
    raw_timestamp = " ".join(tokens[:3])
    time = parser.parse(raw_timestamp)
    # Extract post id
    post_id = tokens[10]
    # Extract username
    username = tokens[13]

    return DoneData(time, post_id, username)


def process_lines(config: Config, lines: List[str]) -> List[DoneData]:
    # Only consider "done"-ed posts
    done_lines = [
        l for l in lines if "process_done" in l and "Moderator override" not in l]

    with open(f"{config.cache_dir}/done.log", "w") as f:
        f.write("\n".join(done_lines))

    dones = [done_line_to_dict(line) for line in done_lines]

    with open(f"{config.cache_dir}/done.json", "w") as f:
        dumps = json.dumps([done.to_dict() for done in dones], indent=2)
        f.write(dumps + "\n")
    
    # Filter dones outside the time frame
    if config.start_date:
        dones = [done for done in dones if done.time > config.start_date]
    if config.end_date:
        # Add a 2 h buffer, to give the transcriber time to mark their transcription as done
        buffer_time = timedelta(hours=2)
        dones = [done for done in dones if done.time < config.end_date + buffer_time]

    return dones


def process_transcription_data(config: Config, dones: List[DoneData]) -> List[Transcription]:
    transcriptions = {}
    cache = {}
    if config.force_cache or not config.no_cache:
        with open(f"{config.cache_dir}/transcriptions.json", encoding='utf8') as f:
            try:
                cache = json.load(f)
            except json.JSONDecodeError:
                cache = {}

    reddit_api = RedditAPI(config)
    with click.progressbar(dones, label="  Fetching transcriptions: ") as pbar:
        for done in pbar:
            # Try to get from cache
            if done.post_id in cache:
                transcriptions[done.post_id] = transcription_from_dict(
                    cache[done.post_id])
            # Get transcription from Reddit
            elif not config.force_cache:
                transcription_comment = reddit_api.get_transcription(
                    done.post_id, done.username)
                if transcription_comment is None:
                    continue
                transcriptions[done.post_id] = transcription_from_comment(
                    transcription_comment)

            with open(f"{config.cache_dir}/transcriptions.json", "w", encoding='utf8') as f:
                json.dump(dict([(key, transcriptions[key].to_dict())
                                for key in transcriptions]), f, ensure_ascii=False, indent=2)

    # Sort by time
    transcription_list = [transcriptions[key] for key in transcriptions]
    transcription_list.sort(key=lambda tr: tr.time)

    # Filter transcriptions outside the time frame
    if config.start_date:
        transcription_list = [tr for tr in transcription_list if tr.time > config.start_date]
    if config.end_date:
        transcription_list = [tr for tr in transcription_list if tr.time < config.end_date]

    return transcription_list


def process_user_gamma_data(config: Config, transcriptions: List[Transcription]) -> UserGammaData:
    user_gamma_data = UserGammaData()

    for transcription in transcriptions:
        user_gamma_data[transcription.username] += 1

    with open(f"{config.cache_dir}/user_gamma.json", "w") as f:
        dumps = json.dumps(user_gamma_data.to_dict(), indent=2)
        f.write(dumps + "\n")

    return user_gamma_data


def process_user_char_data(config: Config, transcriptions: List[Transcription]) -> UserCharData:
    user_char_data = UserCharData()

    for transcription in transcriptions:
        user_char_data[transcription.username] += transcription.characters

    with open(f"{config.cache_dir}/user_chars.json", "w") as f:
        dumps = json.dumps(user_char_data.to_dict(), indent=2)
        f.write(dumps + "\n")

    return user_char_data


def process_sub_gamma_data(config: Config, transcriptions: List[Transcription]) -> SubGammaData:
    sub_gamma_data = SubGammaData()

    for tr in transcriptions:
        sub_gamma_data[tr.subreddit] += 1

    with open(f"{config.cache_dir}/sub_gamma.json", "w") as f:
        dumps = json.dumps(sub_gamma_data.to_dict(), indent=2)
        f.write(dumps + "\n")

    return sub_gamma_data

def process_post_type_data(config: Config, transcriptions: List[Transcription]) -> PostTypeData:
    type_data = PostTypeData()

    for tr in transcriptions:
        type_data[tr.t_type] += 1

    with open(f"{config.cache_dir}/post_types.json", "w") as f:
        dumps = json.dumps(type_data.to_dict(), indent=2)
        f.write(dumps + "\n")

    return type_data
