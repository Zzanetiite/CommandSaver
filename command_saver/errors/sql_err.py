import logging
import sqlite3
from command_saver.constants import log_path
from command_saver.visual_design.formatter import StringFormatter


class SQL_err:
    """
    Class that takes a method and checks for SQL errors and then logs the method's information and errors.
    """

    @staticmethod
    def sql_confirmation(method_description: str, method):
        """
        Takes a method that tries to use sql and tries to execute it, logs this. If it fails,
        error is logged and flagged up to the user.
        Args:
            method_description: the description of the method being executed. This is for logging.
            method: a function that will be executed.
        Returns: method's return value.

        """
        # try to do call the method
        try:
            # Log the event
            logging.info(f"Trying to {method_description}.")
            # call the method
            result = method()
            return result
        # except if SQL crashes
        except sqlite3.Error as e:
            # Log an error in the error file
            logging.error(f"An error occurred when trying {method_description}."
                          f"\nThe error: {e=}, {type(e)=}")
            # Let the user know that an error has occurred.
            StringFormatter(
                text_to_format='An error has occurred.').print_red_bold()
            print(f"Unexpected {e=}, {type(e)=}. See logs in: {log_path}")

    @staticmethod
    def sql_confirmation_2args(method_description: str, method,
                               arg1: str = None,
                               arg2: str = None):
        """
        Takes a method that tries to use sql and tries to execute it, logs this. If it fails,
        error is logged and flagged up to the user.
        Args:
            method_description: the description of the method being executed. This is for logging.
            method: a function that will be executed.
            arg1: argument to pass to the function (a placeholder).
            arg2: another argument to pass to the function (a placeholder).

        Returns: method's return value

        """
        # try to do call the method
        try:
            # Log the event
            logging.info(f"Trying to {method_description}.")
            # call the method
            result = method(arg1, arg2)
            return result
        # except if SQL crashes
        except sqlite3.Error as e:
            # Log an error in the error file
            logging.error(f"An error occurred when trying {method_description}."
                          f"\nThe error: {e=}, {type(e)=}")
            # Let the user know that an error has occurred.
            StringFormatter(
                text_to_format='An error has occurred.').print_red_bold()
            print(f"Unexpected {e=}, {type(e)=}. See logs in: /tmp/cs.log")
