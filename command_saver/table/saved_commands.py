import os
import sqlite3
import time
import logging
from datetime import date
from command_saver.input_window.input_window import InputWindow
from command_saver.table.user_data import UserData
from command_saver.utils.default_database import DefaultDatabase
from command_saver.visual_design.formatter import StringFormatter
from command_saver.errors.sql_err import SQL_err
from command_saver.errors.err import Err
from command_saver.constants import (
    database_path,
    disposition_path,
    mo_t,
    soft_yes_no,
    valid_no,
    valid_yes,
    global_commands
)
from command_saver.string_templates.error_str import *
from command_saver.string_templates.logging_str import *
from command_saver.string_templates.user_prompts import *


class SavedCommands:
    """
    Executes available table actions. Allows to make changes and extract things from Saved Commands table.
    """

    def __init__(self,
                 database_path: str = database_path,
                 command_id: int = None,
                 option: str = None,
                 ):
        """
        Executes commands that table can make.
        Args:
            command_id: The id of the command to be manipulated.
            database_path: database to use for manipulation.
            option: option chosen by user (optional).
        """
        self.command_id = command_id
        self.database = database_path
        self.option = option
        try:
            self.con = sqlite3.connect(self.database)
            if self.con is None:
                Err(error="Connection failed, connection is None. Database loc: {}".format(self.database),
                    msg="connect to the database").error()
            self.cur = self.con.cursor()
        except FileNotFoundError as e:
            Err(error=e, action="locate the database at expected location").error()
            # Create a new database in the expected location
            DefaultDatabase().create_default_database()

    # Private functions support other methods by doing
    # repetitive, multi-choice and multi-path tasks, and also methods & actions
    # are there to keep external calls for them inaccessible.
    # This is to prevent external modules calling the wrong method.

    def commit_and_close_database(self):
        """
        Commits and closes the database opened by the class.

        """
        # Commit the command
        self.con.commit()
        # Close the connection
        self.con.close()

    def print_row_ids(self):
        self.cur.execute(
            "SELECT num_row, command_description, saved_command "
            "FROM saved_commands "
            "ORDER BY num_row"
        )
        list_all_commands = list(self.cur.fetchall())
        print(list_all_commands)
        self.commit_and_close_database()

    def print_all_tables(self):
        self.cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table';")
        list_all_tables = list(self.cur.fetchall())
        print(list_all_tables)
        self.commit_and_close_database()

    def __view_all_saved_commands_method(self):
        """
        Fetches all saved commands from the database.
        Returns: a list of all saved commands from the database.

        """
        # Select all saved entities in the table
        self.cur.execute(
            "SELECT num_row, command_description, saved_command "
            "FROM saved_commands "
            "ORDER BY num_row"
        )
        # Fetch the command list
        list_all_commands = list(self.cur.fetchall())
        # Commit and close the database
        self.commit_and_close_database()
        # return the command list
        return list_all_commands

    def view_all_saved_commands(self):
        """
        Calls the method through sql error checker and step logger.

        """
        msg = f'Trying to fetch all saved commands .'
        # Pass the method to the error checker. This way it only executes when the other function calls it.
        list_all_commands = SQL_err.sql_confirmation(method_description=msg,
                                                     method=self.__view_all_saved_commands_method,
                                                     )
        return list_all_commands

    def recent_commands_list(self):
        """
        Orders the top three most recent saved commands and top eight most popular saved commands
        into a list of firstly, three most recent, then secondly, five most popular, without duplication.
        Returns: a list of recently used commands.

        """
        # Fetch top 3 latest records
        t3l = self.__fetch_top_three_recent()
        # Fetch top 8 most popular records
        t8l = self.__fetch_top_eight_frequent()
        recent_commands_list = []
        # Add all recent commands
        for i in range(len(t3l)):
            recent_commands_list.append(t3l[i])
        # Add popular commands, but not the ones that are also recent
        # because they have already been added.
        # for item in the range of 8 commands or max available
        # if 7 is more than length of command list
        if 7 >= len(t8l) - 1:
            # use shorter length
            r = len(t8l) - 1
        # else
        else:
            # use max length for list to be shown (8 entities)
            r = 7
        for i in range(r):
            # if command is already in the list
            if t8l[i] in recent_commands_list:
                # look at the next command
                continue
            # otherwise (not in the list)
            else:
                # add it to the list
                recent_commands_list.append(t8l[i])
        # return the command list
        return recent_commands_list

    def find_command(self, command_id: int = None):
        """
        Finds a command in the saved commands database table.
        Args:
            command_id: command's id to look for.

        Returns: The value of the command - text that is executed in the terminal.

        """
        # By default, look for the tag defined in the class,
        # but method can be used for other tags as well
        if command_id is None:
            command_id = self.command_id
        else:
            command_id = command_id
        # Try to fetch the command
        try:
            # fetch the tag
            self.cur.execute(
                "SELECT saved_command FROM saved_commands WHERE num_row LIKE ?", (self.command_id,))
            # return the tag in the format of a basic string
            command = ''.join(self.cur.fetchone())
            return command
        # if command was not found
        except TypeError as e:
            # Call the error manager
            Err(error=e, msg='locate the Command ID').error()
            return None
        except ValueError as e:
            # Call the error manager
            Err(error=e, msg='locate the Command ID').error()
            return None
        # if sqlite happened to run into problems
        except KeyError as e:
            msg = "locate the Command ID {}".format(command_id)
            Err(error=e,  msg=msg).error()
        except sqlite3.Error as e:
            # Prepare message for the error
            msg = 'access SQLite, err: %s' % (' '.join(e.args))
            # Call the error manager
            Err(error=e, msg=msg).error()
            return None

    def __risky_action_confirmation(self, action_name: str, action):
        """
        Takes action and asks user to confirm action, which then is found and actioned.
        Args:
            action_name: string, name of the action for dialog confirmation.
            action: a function that will be executed. Takes "command" as an argument.
            Catches SQL exceptions from this action.
        """
        # Look for the command in the database
        command = self.find_command()
        # If None has been returned, command not found
        if command is None:
            # Return to saved commands menu
            return ValueError
        else:
            # Sanity check, is user is sure they want to do the risky action
            msg = RISKY_ACTION_TEMPLATE.format(
                action_name, self.command_id, command, soft_yes_no)
            # Ask user if they are sure they want to delete this?
            confirmation = InputWindow().ask_input(
                msg=msg, valid_answers=valid_yes + valid_no)
            if confirmation in valid_yes:
                # Try to execute the command
                try:
                    logging.info(EXECUTING_COMMAND_TEMPLATE.format(
                        action_name, self.command_id))
                    # by calling the action
                    action(command)
                # Except if something went wrong with Sqlite
                except sqlite3.Error as e:
                    # Prepare message for the error
                    msg = "process {} request with command ID {}".format(
                        action_name, self.command_id)
                    # Call the error manager
                    Err(error=e, msg=msg).error()
            # If they choose not to delete the command,
            if confirmation in valid_no:
                print("{} command stopped.".format(action_name))
                # return to the saved commands menu
                return ValueError
            # If user has chosen to leave and stop the edit
            if confirmation in global_commands:
                # return the global command
                return confirmation

    def delete_command(self):
        """
        Calls the edit command action through confirmation checker,
        because this is a risky action.

        """
        # Pass the action to the function. This way it only executes when the other function calls it.
        self.__risky_action_confirmation(
            "Delete", self.__delete_command_action)

    def __delete_command_action(self, command: str):
        """
        Does the delete steps to delete a command.
        Args:
            command: the terminal command being deleted.

        """
        # Delete the command in the database
        self.cur.execute(
            "DELETE FROM saved_commands WHERE num_row=?", (
                self.command_id,
            )
        )
        # Update num_row values for remaining rows
        self.cur.execute(
            "UPDATE saved_commands SET num_row = num_row - 1 WHERE num_row > ?", (
                self.command_id,
            )
        )
        # Commit the transaction to apply the changes and release the lock
        self.con.commit()
        # Execute the VACUUM command to optimize the database (and reset rows)
        self.cur.execute("VACUUM")
        # Commit delete and close the database
        self.commit_and_close_database()
        # Let the user know that the update has been a success.
        text = SUCCESSFUL_ACTION_TEMPLATE.format(self.command_id, "deleted")
        StringFormatter(text_to_format=text).print_green_bold()

    def execute_command(self,
                        text_to_terminal=False,
                        text_for_terminal=None):
        """
        Executes saved commands.
        Returns: os call with the command or None: command not found.

        """
        if text_to_terminal:
            try:
                logging.info(
                    TEXT_IN_TERMINAL_TEMPLATE.format(text_for_terminal))
                # Run the command in the terminal
                print("----Terminal----")
                return os.system(str(text_for_terminal))
            except OSError as e:
                Err(error=e, msg="execute the command").error()
        # Look for the command in the database
        command_to_execute = self.find_command()
        # If None has been returned, command not found
        if command_to_execute is None:
            # Return to main menu with ValueError and ask user there to try again
            return ValueError
        else:
            # try to execute the command
            try:
                logging.info(
                    "Trying to update popularity and to execute a command.")
                # Update how many times the command has been called
                self.__update_popularity()
                # Save data and close the database.
                self.commit_and_close_database()
                # Run the command in the terminal
                print("----Terminal----")
                return os.system(command_to_execute)
            # except if something goes wrong with OS or sqlite
            except sqlite3.Error as e:
                Err(error=e, msg="update the command's popularity").error()
            except OSError as e:
                Err(error=e, msg="execute the command in terminal using os.system").error()

    def edit_command(self):
        """
        Calls the edit command action through a confirmation checker,
        because this is a risky action.
        """
        # Pass the action to the function. This way it only executes when the other function calls it.
        response = self.__risky_action_confirmation(
            "Edit", self.__edit_command_action)
        # response is given if the user chose to leave
        return response

    def __edit_command_action(self, command: str):
        """
        Does the steps to edit a command.
        Args:
            command: the terminal command being edited.

        """
        # Ask for edit command information
        msg_panel = TEXT_EDIT_TEMPLATE.format(command)
        # Prompt for the new command
        msg = 'Please enter the new command:'
        # Ask the table to submit new command
        new_command = InputWindow().ask_input(msg=msg,
                                              msg_info=msg_panel,
                                              valid_answers='any_string'
                                              )
        # Take the new table command and update the DB
        self.update_command(new_command=str(new_command))
        # Update last_edited field timestamp in the database
        self.__update_timestamp()
        # commit and close the database
        self.commit_and_close_database()
        # Let the user know that the update has been a success.
        msg = "{}, {}".format(self.command_id, command)
        new_command_msg = "updated to {}".format(new_command)
        text = SUCCESSFUL_ACTION_TEMPLATE.format(msg, new_command_msg)
        StringFormatter(text_to_format=text).print_green_bold()

    def add_new_command(self, command_description: str, new_command: str):
        """
        Calls the method through sql error checker and step logger.

        """
        # Pass the method to the error checker. This way it only executes when the other function calls it.
        SQL_err.sql_confirmation_2args(method_description='add a new command.',
                                       method=self.__add_new_command_method,
                                       arg1=command_description,
                                       arg2=new_command)

    def __add_new_command_method(self, command_description: str, new_command: str):
        """
        Adds a new command to the Saved Commands table in the database.

        """
        # generate time and date
        date_today = date.today()
        timestamp_now = time.time()
        # get author
        open_data = UserData(database_path=self.database)
        # call find author to find the author
        author = open_data.find_author()
        # Prepare a row to upload to the database.
        new_command = (
            command_description, new_command, str(
                date_today), int(timestamp_now * 1000), 0, author,
            int(timestamp_now * 1000))
        # add the command to the database
        self.cur.executemany("INSERT INTO saved_commands (command_description, saved_command, "
                             "date_created, timestamp_when_created, times_called, author_name, last_edited)"
                             "VALUES(?, ?, ?, ?, ?, ?, ?)", (new_command,))
        # commit add and close the database
        self.commit_and_close_database()
        # Print the success message
        StringFormatter(
            f'Success! A new command added. Details: '
            f'(command_descr, command, date, timestamp, times called, author, last updated) '
            f'{new_command} .').print_green_bold()

    def update_command(self, new_command):
        """
        Calls the method through sql error checker and step logger.

        """
        msg = f'Trying to update a command {new_command} with command id: {self.command_id}.'
        # Pass the method to the error checker. This way it only executes when the other function calls it.
        SQL_err.sql_confirmation_2args(method_description=msg,
                                       method=self.__update_command_method,
                                       arg1=new_command)

    def __update_command_method(self, new_command, arg2):
        """
        Updates command's data in the database.
        Args:
            new_command: terminal command data to assign to the command_id command.
            arg2: argument needed for the SQL checker. Does nothing.

        """
        # by calling SQL with the new command and command_id
        self.cur.execute(
            "UPDATE saved_commands SET saved_command=? WHERE num_row=?", (new_command, self.command_id,))

    def export_all(self):
        """
        Fetches all commands saved in the database and saves them in a single text file.
        Returns: a disposition document with all database commands.

        """
        # Fetch existing command list
        commands_to_save = self.view_all_saved_commands()
        # Make a file and record the data
        with open(disposition_path, 'w+') as f:
            for line in commands_to_save:
                line = ', '.join(str(v) for v in line) + '\n'
                f.write(line)
        # Let the table know where the file is saved
        msg = disposition_success_str
        StringFormatter(text_to_format=msg).print_green_bold()

    def __update_popularity(self):
        """
        Updates the command's popularity in the database.
        """
        # Try to increment
        try:
            logging.info('Trying to increment the popularity of the command.')
            # Increment times called by one
            self.cur.execute(
                "UPDATE saved_commands SET times_called = times_called + 1 WHERE num_row=?", (self.command_id,))
        # Except if an error is thrown
        except sqlite3.Error as e:
            Err(error=e, msg="increment popularity").error()

    def __update_timestamp(self):
        """
        Updates command's last edited timestamp.
        """
        # Generate timestamp
        timestamp_now = time.time()
        # Try to update the timestamp
        try:
            # log the event
            logging.info(
                TEXT_UPDATE_TIMESTAMP_TEMPLATE.format(self.command_id))
            # Do the update
            self.cur.execute(
                "UPDATE saved_commands SET last_edited=? WHERE num_row=?", (timestamp_now, self.command_id,))
        # Except if an error is thrown
        except sqlite3.Error as e:
            # Prepare message for the error
            msg = "update the timestamp of the command with command_id: {}".format(
                self.command_id)
            # Call the error manager
            Err(error=e, msg=msg).error()

    def __fetch_top_three_recent_method(self):
        """
        Looks at the list of saved commands and return the top 3 latest commands.
        Returns: a list of top three commands with the most recent timestamp.

        """
        # Select all saved entities in the table, order by timestamp
        self.cur.execute(
            "SELECT num_row, command_description, saved_command "
            "FROM saved_commands "
            "ORDER BY timestamp_when_created DESC"
        )
        # fetch the commands
        list_all_commands = list(self.cur.fetchall())
        logging.info(
            "Trying to fetch the top three latest commands from the database. The results: \n{}".format(list_all_commands))
        # Return the commands to the user. Only top 3.
        return list_all_commands[0:3]

    def __fetch_top_three_recent(self):
        """
        Calls the method through sql error checker and step logger.

        """
        # Pass the method to the error checker. This way it only executes when the other function calls it.
        list_of_commands = SQL_err.sql_confirmation(method_description='fetch top three latest commands.',
                                                    method=self.__fetch_top_three_recent_method)
        # return the list of commands
        return list_of_commands

    def __fetch_top_eight_frequent_method(self):
        """
        Looks at the list of saved commands and return the top 8 most popular commands.
        Returns: a list of top eight commands with the highest times called count.

        """
        # Select all saved entities in the table, order by popularity
        self.cur.execute(
            "SELECT num_row, command_description, saved_command "
            "FROM saved_commands "
            "ORDER BY times_called DESC"
        )
        # fetch the commands
        list_all_commands = list(self.cur.fetchall())
        logging.info(
            "Trying to fetch the top eight most popular commands from the database. The results: \n{}".format(list_all_commands))
        # Return the commands to the user. Only top 8.
        return list_all_commands[0:8]

    def __fetch_top_eight_frequent(self):
        """
        Calls the method through sql error checker and step logger.

        """
        # Pass the method to the error checker. This way it oRotaOta-7
        # executes when the other function calls it.
        list_of_commands = SQL_err.sql_confirmation(method_description='fetch top eight most recent commands',
                                                    method=self.__fetch_top_eight_frequent_method)
        # return the list of commands
        return list_of_commands

    def __fetch_one_full_command_method(self):
        """
        Fetches one saved command from the database.
        Returns: a list of all data of that saved command.

        """
        # Select all saved entities in the table
        self.cur.execute(
            "SELECT num_row, command_description, saved_command, date_created, "
            "timestamp_when_created, times_called, author_name, last_edited "
            "FROM saved_commands WHERE num_row LIKE ?", (self.command_id,))
        # Fetch the command list
        one_full_command = list(self.cur.fetchall())
        # Commit and close the database
        self.commit_and_close_database()
        # return the command list
        return one_full_command

    def fetch_one_full_command(self):
        """
        Calls the method through sql error checker and step logger.

        """
        msg = f'Trying to fetch a single long command.'
        # Pass the method to the error checker. This way it only executes when the other function calls it.
        one_full_command = SQL_err.sql_confirmation(method_description=msg,
                                                    method=self.__fetch_one_full_command_method,
                                                    )
        return one_full_command

# print(SavedCommands().print_row_id())
