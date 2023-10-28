from command_saver.constants import log_path
from command_saver.visual_design.formatter import StringFormatter
import logging
# Templates for errors
ERROR_OCCURRED_TEMPLATE = "An error occurred when trying to {}.\nThe error: e={}, type(e)={}"
ERROR_UNEXPECTED_USER_PROMPT_TEMPLATE = "Unexpected error: {}, \n{}."
ERROR_NOT_FOUND = "Error! {} not found."
# Strings
see_logs_str = "See logs in: {}".format(log_path)
error_prompt_str = "Oh no! An error happened."
