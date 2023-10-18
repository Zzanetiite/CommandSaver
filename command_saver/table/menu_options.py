import sqlite3
from command_saver.utils.default_database import DefaultDatabase
from command_saver.errors.sql_err import SQL_err
import logging
from command_saver.constants import database_path


class MenuOptions:
    """Allows to make changes and extract things from Menu Options table."""

    def __init__(self,
                 database_path: str = database_path,
                 ):
        """
        Executes commands that can be done in the table data table.
        Args:
            database_path: database to use.
        """
        self.database = database_path
        # Try to connect to database
        try:
            # Open connection with SQL
            self.con = sqlite3.connect(self.database)
            # Allows to navigate in SQL
            self.cur = self.con.cursor()
        # Except it if database path is not found
        except FileNotFoundError as e:
            # Log an error
            logging.error(f"Database not found error {e=}, {type(e)=}")
            # Then throw an error
            print(f"Unexpected {e=}, {type(e)=}. See logs in: /tmp/cs.log")
            # Create a new database in the expected location
            DefaultDatabase().create_default_database()

    def commit_and_close_database(self):
        """
        Commits and closes the database.

        """
        # commit the command
        self.con.commit()
        # close the connection
        self.con.close()

    def view_options(self):
        """
        Calls the method through sql error checker and step logger.
        """
        # Prepare a message to log
        msg = f'Trying to fetch all menu options from menu options table.'
        # Pass the method to the error checker. This way it only executes when the other function calls it.
        list_all_options = SQL_err.sql_confirmation(method_description=msg,
                                                    method=self.__view_options_method,
                                                    )
        # return a list of menu options
        return list_all_options

    def __view_options_method(self):
        """
        Opens menu data table and fetches the list.
        Returns: list of menu options

        """
        # Select all saved entities in the table
        self.cur.execute(
            "SELECT menu_option_id, option_tag, option_description FROM menu_options ORDER BY menu_option_id"
        )
        # fetch the entities from the table
        list_all_options = list(self.cur.fetchall())
        # close the database
        self.commit_and_close_database()
        # return a list of menu options
        return list_all_options

    def add_option(self, option_to_add):
        # Add to menu options table
        self.cur.executemany(
            "INSERT INTO menu_options (option_tag, option_description, timestamp_when_created)"
            "VALUES(?, ?, ?)", (option_to_add)
        )
        # close the database
        self.commit_and_close_database()
