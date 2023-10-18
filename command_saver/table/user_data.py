import logging
import sqlite3
from command_saver.input_window.input_window import InputWindow
from command_saver.utils.default_database import DefaultDatabase
from command_saver.visual_design.formatter import StringFormatter
from command_saver.errors.sql_err import SQL_err
from command_saver.constants import database_path, global_commands


class UserData:
    """Allows to make changes in the User Data table."""

    def __init__(self,
                 database_path: str = database_path,
                 ):
        """
        Executes commands that can be done in the table.
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

    # Private function support other methods by doing
    # repetitive, multi-choice and multi-path tasks, and also methods & actions
    # are there to keep external calls for them inaccessible.
    # This is to prevent external modules calling the wrong method.

    def commit_and_close_database(self):
        """
        Commits and closes the database.

        """
        # commit the command
        self.con.commit()
        # close the connection
        self.con.close()

    def find_author(self):
        """
        Calls the method through sql error checker and step logger.
        """
        # Prepare a message for the log
        msg = f'Trying to fetch the author from user data table.'
        # Pass the method to the error checker. This way it only executes when the other function calls it.
        author = SQL_err.sql_confirmation(method_description=msg,
                                          method=self.__find_author_method,
                                          )
        # Return the author
        return author

    def __find_author_method(self):
        """
        Finds the saved author from the user data table.
        Returns: a string: author

        """
        # Fetch the username from the data table
        self.cur.execute(
            "SELECT username FROM user_data")
        # Format author into a simple string
        author = ''.join(self.cur.fetchone())
        # Close the database, because this function can be called from external modules.
        self.commit_and_close_database()
        # Return the author
        return author

    def change_author(self):
        """
        Calls the method through sql error checker and step logger.
        """
        print("in author change function")
        # Prepare a message for the log
        msg = f'Trying to change the author from user data table.'
        # Pass the method to the error checker. This way it only executes when the other function calls it.
        author = SQL_err.sql_confirmation(method_description=msg,
                                          method=self.__change_author_method,
                                          )
        # return author
        return author

    def __change_author_method(self):
        """
        Changed the author from the user data table.

        """
        # Find the author to edit.
        existing_author = self.find_author()
        # Reopen the connection
        self.con = sqlite3.connect(self.database)
        self.cur = self.con.cursor()
        # get new author's name
        new_author = InputWindow().ask_input(msg='Please enter the new author name:',
                                             msg_info=f'Change author command selected. '
                                                      f'Current author: {existing_author}',
                                             valid_answers='any_string'
                                             )
        # If user has chosen to leave
        if new_author in global_commands:
            # return the global command
            return new_author
        # Update the author's data
        self.cur.execute(
            "UPDATE user_data SET username=? WHERE username=?",
            (new_author, existing_author))
        # Close the database
        self.commit_and_close_database()
        # Print the success message
        text = f"Author successfully changed from {existing_author} to  {new_author}."
        StringFormatter(text_to_format=text).print_green_bold()

    def change_authors_department(self):
        """
        Calls the method through sql error checker and step logger.
        """
        # Prepare a message for the log
        msg = f"Trying to change the author's department in the user data table."
        # Pass the method to the error checker. This way it only executes when the other function calls it.
        department = SQL_err.sql_confirmation(method_description=msg,
                                              method=self.__change_authors_department_method,
                                              )
        # Return the department
        return department

    def __change_authors_department_method(self):
        """
        Changed the author's department from the user data table.

        """
        # Find the department to edit.
        self.cur.execute(
            "SELECT department FROM user_data")
        # get the existing department
        existing_department = ''.join(self.cur.fetchone())
        # ask for new department's name
        new_department = InputWindow().ask_input(msg="Please enter the department/team.",
                                                 msg_info=f'Change department command selected. Current department: {existing_department}',
                                                 valid_answers='any_string'
                                                 )
        print(new_department)
        # If user has chosen to leave
        if new_department in global_commands:
            # return the global command
            return new_department
        # Update the department data
        self.cur.execute(
            "UPDATE user_data SET department=? WHERE department=?",
            (new_department, existing_department))
        # close the database
        self.commit_and_close_database()
        # Print the success message
        text = f"Department successfully changed from {existing_department} to  {new_department}."
        StringFormatter(text_to_format=text).print_green_bold()
