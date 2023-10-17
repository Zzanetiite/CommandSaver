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

# Menu options - these cannot be changed by the user, but if admin chooses to, they can do it here.
timestamp_now = time.time()
menu_options_data = [
    ('e', 'Execute an existing command', int(timestamp_now * 1000)),
    ('a', 'Add a new command', int(timestamp_now * 1000)),
    ('edit', 'Edit an existing command', int(timestamp_now * 1000)),
    ('d', 'Delete a command', int(timestamp_now * 1000)),
    ('ss', 'Show single command full data ', int(timestamp_now * 1000)),
    ('t', 'Write a command directly for the terminal', int(timestamp_now * 1000)),
    ('b', 'Go to the Main Menu', int(timestamp_now * 1000)),
    ('bs', 'Go to the Saved Commands Menu', int(timestamp_now * 1000)),
    ('help', 'Go to the Help Page', int(timestamp_now * 1000)),
    ('r', 'Repeat last command', int(timestamp_now * 1000)),
    ('q', 'Exit program', int(timestamp_now * 1000)),
    ('exportall', 'Export all saved commands to a text file.', int(timestamp_now * 1000)),
    ('setuser', "Set user's name.", int(timestamp_now * 1000)),
    ('setuserdep', "Set user's department.", int(timestamp_now * 1000)),
]

version = '2.1.1'

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
intermediate_menu_info = [
    'What would you like to do next?', usage, prompt]
