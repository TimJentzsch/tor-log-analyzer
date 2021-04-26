from os import makedirs
import matplotlib.pyplot as plt

from tor_log_analyzer.config import Config
from tor_log_analyzer.data_processors import process_lines, process_sub_gamma_data, process_transcription_data, process_user_char_data, process_user_gamma_data
from tor_log_analyzer.stat_generators import generate_format_stats, generate_history, generate_sub_stats, generate_type_stats, generate_user_count_length_stats, generate_user_gamma_stats, generate_user_max_length_stats


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

    # Process data
    dones = process_lines(config, lines)
    user_gamma_data = process_user_gamma_data(config, dones)
    transcription_data = process_transcription_data(config, dones)
    sub_gamma_data = process_sub_gamma_data(config, transcription_data)
    user_char_data = process_user_char_data(config, transcription_data)

    # Generate stats
    generate_history(config, dones)
    generate_user_gamma_stats(config, user_gamma_data)
    generate_sub_stats(config, sub_gamma_data)
    generate_type_stats(config, transcription_data)
    generate_format_stats(config, transcription_data)
    generate_user_count_length_stats(config, user_gamma_data, user_char_data)
    generate_user_max_length_stats(config, user_char_data)
