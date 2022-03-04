"""
    Version 1.0 basic source with lots of print
"""
import os
import shutil
import logging
from ChessControllers import ChessMainControllers
from ChessViews import ChessMainViews
from ChessModels import ChessMainModels

DEFAULT_LOGGING_DIR = 'c:/temp/P4/'
DEFAULT_LOGGING_FILE_NAME = 'log.txt'

def clean_up_log():
    """Recreate all directories and files obtained in a previous run
    Raise an exception in case of error.
    """
    try:
        if not os.path.isdir(DEFAULT_LOGGING_DIR):
            os.makedirs(DEFAULT_LOGGING_DIR)

    except Exception as error:
        print(f'Unexpected exception in clean_up_previous_results(): {error}')

def start_logging():
    """Create a debug log file
    Raise an exception in case of errors.
    """
    try:
        logging_file_path = DEFAULT_LOGGING_DIR + DEFAULT_LOGGING_FILE_NAME
        if os.path.isfile(logging_file_path):
            os.remove(logging_file_path)

        if not os.path.isdir(DEFAULT_LOGGING_DIR):
            os.makedirs(DEFAULT_LOGGING_DIR)

        open(logging_file_path, 'w').close()

        logging.basicConfig(filename=logging_file_path, level=logging.DEBUG,
                            format='%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s')
        logging.debug("start_logging")

    except Exception as error:
        print(f'Unexpected exception in start_logging(): {error}')

def main():
    clean_up_log()
    start_logging()
    # self.my_view = ChessMainViews.ChessMainView()
    # self.my_model = ChessMainModels.ChessMainModel()
    chess_main_controller = ChessMainControllers.ChessMainController(ChessMainViews.ChessMainView(), ChessMainModels.ChessMainModel())
    chess_main_controller.run()


if __name__ == "__main__":
    main()
