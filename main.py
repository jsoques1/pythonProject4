"""
    Version 1.0 basic source with lots of print
    Version 1.1 players management added
    Version 1.2 tournaments management added
    Version 1.3 reports management added
"""
import os
import configparser
import logging
from ChessControllers import ChessMainControllers
from ChessViews import ChessMainViews
from ChessModels import ChessMainModels


def read_main_section_config_file():
    config = configparser.ConfigParser()
    config.read('MyChessApp.ini')
    log_dir = config['main']['log_dir']
    log_file = config['main']['log_file']
    log_level = config['main']['log_level']

    return log_dir, log_file, log_level


def clean_up_log(log_dir):
    """Recreate all directories and files obtained in a previous run
    Raise an exception in case of error.
    """
    try:
        if not os.path.isdir(log_dir):
            os.makedirs(log_dir)

    except Exception as error:
        print(f'Unexpected exception in clean_up_previous_results(): {error}')


def start_logging(log_dir, log_file, log_level):
    """Create a debug log file
    Raise an exception in case of errors.
    """
    try:
        logging_file_path = log_dir + '/' + log_file
        if os.path.isfile(logging_file_path):
            os.remove(logging_file_path)

        if not os.path.isdir(log_dir):
            os.makedirs(log_dir)

        open(logging_file_path, 'w').close()

        logging.basicConfig(filename=logging_file_path, level=log_level,
                            format='%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s')
        logging.debug("start_logging")

    except Exception as error:
        print(f'Unexpected exception in start_logging(): {error}')


def main():
    log_dir, log_file, log_level = read_main_section_config_file()
    clean_up_log(log_dir)
    start_logging(log_dir, log_file, log_level)
    chess_main_controller = ChessMainControllers.ChessMainController(ChessMainViews.ChessMainView(),
                                                                     ChessMainModels.ChessMainModel())
    chess_main_controller.run()


if __name__ == "__main__":
    main()
