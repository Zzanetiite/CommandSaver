import logging
import sqlite3
from command_saver.string_templates.logging_str import *
from command_saver.string_templates.error_str import *
from command_saver.errors.err import Err


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
            logging.info(LOG_ACTION_TEMPLATE.format(method_description))
            # call the method
            result = method()
            return result
        # except if SQL crashes
        except sqlite3.Error as e:
            Err(error=e, action=method_description).error()

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
            logging.info(LOG_ACTION_TEMPLATE.format(method_description))
            # call the method
            result = method(arg1, arg2)
            return result
        # except if SQL crashes
        except sqlite3.Error as e:
            Err(error=e, action=method_description).error()
