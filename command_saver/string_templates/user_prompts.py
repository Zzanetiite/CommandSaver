from command_saver.constants import (disposition_path)
# Templates for user prompts
VALID_ANSWERS_TEMPLATE = "Valid answers: {}"
SORRY_NOT_VALID_TEMPLATE = "Sorry! {} is not a valid answer. Please try again or exit."
RISKY_ACTION_TEMPLATE = "Are you sure you want to {} the command {}: {}? {}"
SUCCESSFUL_ACTION_TEMPLATE = "Success! Command with ID: {} has been {}."
TEXT_IN_TERMINAL_TEMPLATE = "Trying to execute text into terminal. The text: {}"
TEXT_EDIT_TEMPLATE = "\nEdit command selected, command being edited: {}"
TEXT_UPDATE_TIMESTAMP_TEMPLATE = "Trying to update timestamp of the command with commadn_id: {}."
TEXT_AUTHOR_SUCCESS = "Author successfully changed from {} to {}."
TEXT_DEPARTMENT_SUCCESS = "Department successfully changed from {} to {}."
TEXT_DATABASE_EXISTS = "Database exists. The command cancelled and a new database not created. \nDatabase location: {}"

# Strings
disposition_success_str = "Successfully saved at: {}".format(disposition_path)
