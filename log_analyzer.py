#!/usr/bin/env python
from typing import List, Dict
import json
from datetime import datetime
import cli.app
from dateutil import parser
import matplotlib.pyplot as plt

class DoneInfo:
    def __init__(self, time: datetime, post_id: str, username: str):
        self._time = time
        self._post_id = post_id
        self._username = username

    @property
    def time(self) -> datetime:
        return self._time

    @property
    def timestamp(self) -> str:
        return self.time.__str__()

    @property
    def post_id(self) -> str:
        return self._post_id

    @property
    def username(self) -> str:
        return self._username

    def to_dict(self) -> Dict:
        return {
            'timestamp': self.timestamp,
            'post_id': self.post_id,
            'username': self.username,
        }

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

def generate_user_stats(app, dones: List[DoneInfo]):
    user_data = {}

    for done in dones:
        user = done.username
        if user in user_data:
            user_data[user] += 1
        else:
            user_data[user] = 1

    with open(f"{app.params.output}/user_gamma.json", "w") as f:
        dumps = json.dumps(user_data, indent=2)
        f.write(dumps + "\n")

    labels = [username for username in user_data]
    data = [user_data[username] for username in user_data]

    plt.barh(labels, data)
    plt.show()

def process_lines(app, lines: List[str]):
    # Only consider "done"ed posts
    done_lines = [l for l in lines if "process_done" in l and "Moderator override" not in l]

    with open(f"{app.params.output}/done.log", "w") as f:
        f.write("\n".join(done_lines))

    dones = [done_line_to_dict(line) for line in done_lines]

    with open(f"{app.params.output}/done.json", "w") as f:
        dumps = json.dumps([done.to_dict() for done in dones], indent=2)
        f.write(dumps + "\n")

    generate_user_stats(app, dones)

@cli.app.CommandLineApp
def log_analyzer(app):
    input_file = app.params.input
    with open(input_file) as f:
        lines = f.read().splitlines()
        process_lines(app, lines)

# Set CLI parameters
log_analyzer.add_param("-i", "--input", help="the path to the input file", default="input/input.log", type=str)
log_analyzer.add_param("-o", "--output", help="the path to the output folder", default="output", type=str)

if __name__ == "__main__":
    log_analyzer.run()
