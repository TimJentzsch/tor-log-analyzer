# tor-log-analyzer

A tool to create statistics from the bot logs of r/TranscribersOfReddit.

## Installation

First, make sure you have the prerequisites installed:
- Python
- Pip

Clone the project:

```sh
# Using HTTPS:
$ git clone https://github.com/TimJentzsch/tor-log-analyzer.git
# Using SSH:
$ git clone git@github.com:TimJentzsch/tor-log-analyzer.git
# Using GitHub CLI:
$ gh repo clone TimJentzsch/tor-log-analyzer
```

Navigate to the folder:

```sh
$ cd tor-log-analyzer
```

Install the dependencies:

```sh
$ pip install -r requirements.txt
```

## Usage

Put the log file that you want to analyze in `input/input.log`. Then run the tool:

```sh
$ ./log_analyzer.py
# Or use python directly:
$ python log_analyzer.py
```

The stats will be put in `output/` by default. A lot of the behavior and colors can be configured. Use the help command to find out more:

```
$ ./log_analyzer.py -h
```
