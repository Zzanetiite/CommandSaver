import logging
from command_saver.visual_design.formatter import StringFormatter
from command_saver.constants import log_path
from command_saver.string_templates.logging_str import *
from command_saver.string_templates.error_str import *


class Err(object):
    """
    Logs the error and prints an error message in the terminal.
    """

    def __init__(self,
                 error,
                 action: str,
                 logs: str = log_path):
        """
        Takes errors, logs and formats them.
        Args:
            error: error text, object, message that is returned with the error.
            action: message to display in the error.
            logs: path to logs location.
        """
        self.e = error
        self.logs = logs
        self.action = action

    def error(self):
        logging.error(ERROR_OCCURRED_TEMPLATE.format(
            self.action, self.e, type(self)))
        StringFormatter(text_to_format=error_prompt_str).print_red_bold()
        print(ERROR_UNEXPECTED_USER_PROMPT_TEMPLATE.format(
            self.e, see_logs_str))
        print(see_logs_str)
