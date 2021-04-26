from os import makedirs
import matplotlib.pyplot as plt
import time
import click

from tor_log_analyzer.config import Config
from tor_log_analyzer.data_processors import process_lines, process_sub_gamma_data, process_transcription_data, process_user_char_data, process_user_gamma_data, process_post_type_data
from tor_log_analyzer.stat_generators import generate_format_stats, generate_history, generate_sub_stats, generate_type_stats, generate_user_count_length_stats, generate_user_gamma_stats, generate_user_max_length_stats, generate_general_stats


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
    plt.rcParams['grid.color'] = colors.line
    plt.rcParams['grid.alpha'] = 0.8


def analyze_logs(config: Config):
    """
    Analyze the logs with the given configuration.
    """

    start = time.time()
    click.echo("Configuring data.")

    # Create all needed directories
    try:
        makedirs(config.output_dir)
        makedirs(config.cache_dir)
        makedirs(config.image_dir)
    except OSError as _:
        pass

    configure_plot_style(config)


    click.echo("Processing data:")
    # Read the logs and process them
    with open(config.input_file) as f:
        lines = f.read().splitlines()
        process_lines(config, lines)
    # Process data
    click.echo("  Processing logs.")
    dones = process_lines(config, lines)
    click.echo("  Processing users.")
    user_gamma_data = process_user_gamma_data(config, dones)
    transcription_data = process_transcription_data(config, dones)
    click.echo("  Processing transcriptions.")
    user_char_data = process_user_char_data(config, transcription_data)
    click.echo("  Processing post types.")
    post_type_data = process_post_type_data(config, transcription_data)
    click.echo("  Processing subreddits.")
    sub_gamma_data = process_sub_gamma_data(config, transcription_data)

    click.echo("Generating stats:")
    # Generate stats
    click.echo("  Generating general stats.")
    generate_general_stats(config, user_gamma_data, sub_gamma_data, transcription_data, post_type_data)
    click.echo("  Generating history chart.")
    generate_history(config, dones)
    click.echo("  Generating user transcription count chart.")
    generate_user_gamma_stats(config, user_gamma_data)
    click.echo("  Generating subreddit transcription count chart.")
    generate_sub_stats(config, sub_gamma_data)
    click.echo("  Generating transcription format chart chart.")
    generate_format_stats(config, transcription_data)
    click.echo("  Generating transcription type chart.")
    generate_type_stats(config, post_type_data)
    click.echo("  Generating transcription length chart.")
    generate_user_max_length_stats(config, user_char_data)
    click.echo("  Generating transcription count vs. length chart.")
    generate_user_count_length_stats(config, user_gamma_data, user_char_data)

    end = time.time()
    duration = int((end - start))
    click.echo(f"Done in {duration} s.")
