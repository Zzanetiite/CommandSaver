import logging

from command_saver.visual_design.formatter import StringFormatter
from command_saver.constants import log_path


class Err:
    """
    Logs the error and prints an error message in the terminal.
    """

    def __init__(self,
                 error,
                 msg: str,
                 logs: str = log_path):
        """
        Takes errors, logs and formats them.
        Args:
            error: error text, object, message that is returned with the error.
            msg: message to display in the error.
            logs: path to logs location.
        """
        self.e = error
        self.logs = logs
        self.msg = msg

    def error(self):
        # Log the error
        logging.error(
            f'Oh no! An error has occurred: {self.e=}, {type(self.e)=}. See logs in: {self.logs}')
        # Let the user know that an error has occurred
        StringFormatter(text_to_format=self.msg).print_red_bold()
        # and return None, stands for: nothing was found
