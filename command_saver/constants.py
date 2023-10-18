from os import path, makedirs
import time

# Path for logs
directory = path.expanduser("~")
folder = 'command_saver'
filename = 'cs.log'
log_path = path.join(directory, folder, filename)
disposition_path = path.join(directory, folder, 'disposition.txt')
# Path for default database location to be in user's home directory
database_path: str = path.join(directory, folder, 'command_saver.db')
# Create the directory if it doesn't exist
makedirs(path.dirname(log_path), exist_ok=True)


class MenuOption:
    """Class to hold the menu options data."""

    def __init__(self, key: str, name: str, description: str):
        self.key = key
        self.name = name
        self.description = description


# Create instances of MenuOption for each menu option
mo_e = MenuOption('e', 'execute', 'Execute an existing command')
mo_a = MenuOption('a', 'add', 'Add a new command')
mo_edit = MenuOption('edit', 'edit', 'Edit an existing command')
mo_d = MenuOption('d', 'delete', 'Delete a command')
mo_ss = MenuOption('ss', 'show single', 'Show single command full data')
mo_t = MenuOption('t', 'terminal', 'Write a command directly for the terminal')
mo_mm = MenuOption('mm', 'main menu', 'Go to the Main Menu')
mo_scm = MenuOption('scm', 'saved commands menu',
                    'Go to the Saved Commands Menu')
mo_help = MenuOption('h', 'help', 'Go to the Help Page')
mo_r = MenuOption('r', 'repeat', 'Repeat last command')
mo_q = MenuOption('q', 'quit', 'Exit program')
mo_exp = MenuOption(
    'exp', 'export', 'Export all saved commands to a text file.')
mo_username = MenuOption('user', 'username', "Set user's name.")
mo_userdep = MenuOption('setuserdep', 'user department',
                        "Set user's department.")

# Menu options - these cannot be changed by the user, but if admin chooses to, they can do it here.
timestamp_now = time.time()

menu_options_to_include = [
    mo_e, mo_d, mo_a, mo_edit, mo_ss, mo_t, mo_mm, mo_scm, mo_help, mo_r, mo_q, mo_exp, mo_username, mo_userdep,
]

# Create a list of tuples excluding the timestamp
menu_options_data = [(menu_option.key, menu_option.description, timestamp_now)
                     for menu_option in menu_options_to_include]

print(
    f"Trying out the access to menu commands: {mo_a.key}, and descr {mo_a.description}")


version = '2.1.2'

# Prepare prompt and usage instructions to use in all layouts.
prompt = 'Please select one of the available Menu Options or an option and a command.\n'
usage = 'Usage: [OPTION] [COMMAND]'
using_from_terminal = '\nTo use CommandSaver directly from the terminal, set an alias for the program, like so:\n' + \
    'alias cs="python "...your/path/to/program/CommandSaver/command_saver/cs.py"\n' + \
    'Add it to PYPATH, and then call the options with commands using:\n' + \
    '[ALIAS] [OPTION] [COMMAND]'
# Prepare contents for each of the layouts
help_menu_info = ['Help Page', 'Application version: ', version,
                  '\n', usage,
                  'This is a command line interface application that is used the same way as aliases, '
                  'but meant for longer and more complex commands.',
                  using_from_terminal]
main_menu_info = ['Main Menu', usage, prompt]
saved_commands_info = ['Saved Commands', usage, prompt]

# Valid user answers when answering yes or no questions
soft_yes_no = '(y/N)'
valid_yes = ['Y', 'y', 'yes', 'Yes', 'YES', '']
valid_no = ['N', 'n', 'No', 'no', 'NO']

global_commands = [mo_q.key, mo_mm.key, mo_scm.key, mo_help]

items_before_break = [
    mo_e.key, mo_a.key, mo_edit.key, mo_d.key, mo_t.key, mo_r.key, mo_ss.key,
]

options_within_main_menu = [
    mo_e.key, mo_a.key, mo_edit.key, mo_d.key, mo_ss.key, mo_t.key, mo_help.key, mo_q.key, mo_mm.key, mo_r.key
]

options_within_input_menu = [
    mo_q.key, mo_mm.key, mo_scm.key,
]
