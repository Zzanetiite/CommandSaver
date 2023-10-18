import sqlite3
from datetime import date
import time
from pathlib import Path
from os import remove
from command_saver.input_window.input_window import InputWindow
from command_saver.visual_design.formatter import StringFormatter
from command_saver.constants import (
    menu_options_data,
    database_path,
    valid_no,
    valid_yes
)


class DefaultDatabase:
    """
    Creates default database for CommandSaver program.
    To be used if the database has been accidentally
    deleted by the table.
    """

    def __init__(self,
                 mock_database_path: str = None):
        # Prepare placeholders
        self.existing_data = None
        self.existing_data_path = None
        # Only taking the mock path because if not provided,
        # we assume that it is normal database setup, which has a static database location.
        self.mock_database_path = mock_database_path
        # If call is not a test, then it is a default database set up for a missing database,
        # so set database path to the expected program database location
        if self.mock_database_path is None:
            try:
                self.database_path = database_path
            except sqlite3.Error as e:
                print(f"SQLite error: {e}")

            except Exception as e:
                print(f"An error occurred: {e}")

        # otherwise, assume it is a test and
        else:
            # use the path given to the class: the mock math.
            self.database_path = mock_database_path

        # Prepare information to use for record-keeping
        self.date_today = date.today()
        self.timestamp_now = time.time()
        self.author = 'admin'

        # Default saved commands that table can use as soon as they launch the program
        self.saved_commands_data = [
            ('Check git status', 'git status', str(self.date_today), int(self.timestamp_now * 1000), 2,
             self.author, int(self.timestamp_now * 1000)),
            ('Add all git command', 'git add --all', str(self.date_today), int(self.timestamp_now * 1000), 0,
             self.author, int(self.timestamp_now * 1000)),
            ('Git log', 'git log --oneline', str(self.date_today), int(self.timestamp_now * 1000), 4,
             self.author, int(self.timestamp_now * 1000)),
            ('Hello world!', 'echo "Hello world!"', str(self.date_today), int(self.timestamp_now * 1000), 5,
             self.author, int(self.timestamp_now * 1000)),
        ]
        # Menu options - these cannot be changed by the user, but if admin chooses to, they can do it here.
        self.menu_options_data = menu_options_data
        # User information
        self.user_data = [
            ('admin', 'administration'),
        ]

    def delete_database(self):
        """
        Deletes the database.
        """
        remove(self.database_path)

    def keep_backup(self):
        """
        Checks the backup folder and if there is back up returns True.
        If the backup exists, asks the user to choose what to do with it: delete or keep.
        Returns: True (backup exists) or False (backup does not exist)
        """
        # If this is a test, don't check the backup
        if self.mock_database_path is not None:
            return False
        # otherwise, this class creates a default database
        else:
            # Check whether database exists already
            if Path(self.database_path).is_file():
                # If it does, ask if the user is sure they want to replace it
                user_choice = InputWindow().ask_input(msg='Please choose Yes (delete) or No (keep): ',
                                                      msg_info='Database found, would you like to delete all '
                                                               'data and create a new database with default data?',
                                                      valid_answers=valid_yes + valid_no

                                                      )
                # If user chooses to delete the backup
                if user_choice in valid_yes:
                    # delete the backup
                    self.delete_database()
                    # and return False (back up does not exist)
                    return False
                # If user chooses to keep the backup
                elif user_choice in valid_no:
                    # return True (back up exists, we want to keep it)
                    return True
            # If database does not exist already
            else:
                # return False (back up does not exist)
                return False

    def __create_saved_commands_table(self, cur):
        """
        Creates saved commands table in Sqlite database.
        Args:
            cur: sqlite cursor.
        """
        # Create table in sqlite3
        cur.execute("CREATE table saved_commands ("
                    "command_id INTEGER NOT NULL PRIMARY KEY, "
                    "command_description TEXT, "
                    "saved_command TEXT NOT NULL, "
                    "date_created TEXT, "
                    "timestamp_when_created INTEGER, "
                    "times_called INTEGER, "
                    "author_name TEXT NOT NULL,"
                    "last_edited INTEGER)")
        # Add data to the table
        cur.executemany("INSERT INTO saved_commands (command_description, saved_command, "
                        "date_created, timestamp_when_created, times_called, author_name, last_edited)"
                        "VALUES(?, ?, ?, ?, ?, ?, ?)", self.saved_commands_data)

    def __create_menu_options_table(self, cur):
        """
        Creates menu options user in Sqlite database.
        Args:
            cur: sqlite cursor.
        """
        # Create table in sqlite
        cur.execute("CREATE table menu_options ("
                    "menu_option_id INTEGER NOT NULL PRIMARY KEY, "
                    "option_tag TEXT NOT NULL UNIQUE,"
                    "option_description TEXT NOT NULL,"
                    "timestamp_when_created INTEGER)")
        # Add data to the table
        cur.executemany("INSERT INTO menu_options (option_tag, option_description, timestamp_when_created)"
                        "VALUES(?, ?, ?)", self.menu_options_data)

    def __create_user_data_table(self, cur):
        """
        Creates recent commands table from saved commands.
        Args:
            cur: sqlite cursor.
        """
        # Create recent commands table
        cur.execute("CREATE table user_data ("
                    "user_data_id INTEGER NOT NULL PRIMARY KEY, "
                    "username TEXT NOT NULL, "
                    "department TEXT NOT NULL)")
        # Add data to the table
        cur.executemany("INSERT INTO user_data (username, department)"
                        "VALUES(?, ?)", self.user_data)

    def create_default_database(self):
        """
        Creates a database with 3 users: saved commands,
        menu options and recent commands.
        """
        # If database exists and user chooses to keep it
        if self.keep_backup():
            return f"Database exists. The command cancelled and a new database not created. \n" \
                   f"Database location: {self.database_path}"
        # If it doesn't exist or has been deleted
        else:
            # Open connection with SQL
            con = sqlite3.connect(self.database_path)
            # Allows to navigate in SQL
            cur = con.cursor()
            # Create tables
            self.__create_saved_commands_table(cur)
            self.__create_menu_options_table(cur)
            self.__create_user_data_table(cur)
            # Commit the data
            con.commit()
            # Close the connection
            con.close()
            # Print the success message to the user
            StringFormatter(
                text_to_format='Success! Database created.').print_green_bold()
