from os import path
import command_saver
import time

# Path for logs
directory = path.dirname(command_saver.__file__)
folder = 'data'
filename = 'cs.log'
log_path = path.join(directory, folder, filename)
# Path for default database location
database_path: str = path.join(directory, folder, 'command_saver.db')

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


