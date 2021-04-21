#!/usr/bin/env python
from typing import List, Dict, Tuple
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

    top_count = app.params.top

    # Sort by user gamma
    sorted_data: List[Tuple[str, int]] = [(username, user_data[username]) for username in user_data]
    sorted_data.sort(key=lambda e: e[1], reverse=True)
    # Aggregate the rest of the users that didn't make it in the top to a single entry
    rest: List[Tuple[str, int]] = [("Other", sum([entry[1] for entry in sorted_data[top_count:]]))]
    # Extract the top users
    top_list = sorted_data[:top_count]
    top_list.reverse()
    # Merge everything together
    compressed_data: List[Tuple[str, int]] = rest + top_list

    labels = [entry[0] for entry in compressed_data]
    data = [entry[1] for entry in compressed_data]

    colors = [app.params.secondarycolor] + [app.params.primarycolor for _ in range(len(top_list))]

    plt.barh(labels, data, color=colors)
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

    # Set plot colors
    plt.rcParams['figure.facecolor'] = app.params.backgroundcolor
    plt.rcParams['axes.facecolor'] = app.params.backgroundcolor
    plt.rcParams['axes.edgecolor'] = app.params.linecolor
    plt.rcParams['text.color'] = app.params.textcolor
    plt.rcParams['xtick.color'] = app.params.linecolor
    plt.rcParams['xtick.labelcolor'] = app.params.textcolor
    plt.rcParams['ytick.color'] = app.params.linecolor
    plt.rcParams['ytick.labelcolor'] = app.params.textcolor

    with open(input_file) as f:
        lines = f.read().splitlines()
        process_lines(app, lines)

# Set CLI parameters
log_analyzer.add_param("-i", "--input", help="the path to the input file", default="input/input.log", type=str)
log_analyzer.add_param("-o", "--output", help="the path to the output folder", default="output", type=str)
log_analyzer.add_param("-t", "--top", help="the number of entires in the top X diagrams", default=10, type=int)

log_analyzer.add_param("--primarycolor", help="the primary color to use in the graphs", default="#80cbc4", type=str)
log_analyzer.add_param("--secondarycolor", help="the secondary color to use in the graphs", default="#438078", type=str)
log_analyzer.add_param("--backgroundcolor", help="the background color to use in the graphs", default="#232323", type=str)
log_analyzer.add_param("--textcolor", help="the text color to use on the background color", default="#fff", type=str)
log_analyzer.add_param("--linecolor", help="the text color to use on the background color", default="#484848", type=str)

if __name__ == "__main__":
    log_analyzer.run()
