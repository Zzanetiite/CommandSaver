import os
import sqlite3
import unittest
from command_saver.table.saved_commands import SavedCommands
from unittest.mock import patch
from command_saver.utils.default_database import DefaultDatabase
import command_saver
from os import path


class TestSavedCommands(unittest.TestCase):
    mock_database_path = 'tests/data/command_saver.db'
    data_sample = ('Say hello', '$echo Hello dearest world',
                   'date_today', 1234567890123, 0, 'admin', 1234567890123)
    """
    Tests SavedCommands parameters and methods.
    """

    def setUp(self):
        """
        Create a test database before every unit test.

        """
        # create a mock database
        self.mock_database = DefaultDatabase(self.mock_database_path)
        self.mock_database.create_default_database()
        self.original_saved_commands_table = self.mock_database.saved_commands_data

    def tearDown(self):
        """
        Delete the test database after every test.

        """
        # delete mock database
        self.mock_database.delete_database()

    @patch('command_saver.table.saved_commands.sqlite3.connect')
    def test_parameters_exist(self, mock_connect_to_db):
        """
        Test whether parameters have been defined successfully.
        Test whether database is called when object is created.
        Args:
            mock_connect_to_db: mock database connection call.

        """
        dummy_id = 1
        # Arrange
        dummy_path = 'dummy_path.db'
        mock_object = SavedCommands(command_id=dummy_id,
                                    database_path=dummy_path,
                                    )
        # Assert
        self.assertEqual(dummy_id, mock_object.command_id)
        self.assertEqual(dummy_path, mock_object.database)
        mock_connect_to_db.assert_called_once_with(dummy_path)

    @patch('command_saver.table.saved_commands.InputWindow')
    def test_delete_command(self, mock_input_window):
        """
        test whether delete command deletes an entity.
        Other use cases are tested in the test_run_me.py
        Args:
            mock_input_window: mock user input.

        """
        # Arrange
        command_id = 1
        # create a mock command for the happy path
        mock_user_command = SavedCommands(command_id=command_id,
                                          database_path=self.mock_database_path,
                                          )
        # Mock the response for the sanity check
        mock_input_window().ask_input.return_value = 'Y'
        # Delete the element from the list to get the expected result
        expected_result = self.indexed_table(
            self.original_saved_commands_table)
        expected_result.pop(0)
        expected_result.sort()
        # Act
        # delete the command
        mock_user_command.delete_command()
        # reopen the database
        mock_user_command_test = SavedCommands(
            database_path=self.mock_database_path)
        # and check if the row exists
        mock_user_command_test.cur.execute(
            "SELECT num_row, command_description, saved_command, date_created,"
            "timestamp_when_created, times_called, "
            "author_name, last_edited FROM saved_commands ORDER BY command_id")
        result = list(mock_user_command_test.cur.fetchall())
        # close the database
        mock_user_command_test.commit_and_close_database()
        # Assert
        self.assertEqual(expected_result, result)

    def test_add_new_command(self):
        """
        To test whether a command is added to the database successfully.

        """
        # create a mock command to work with
        mock_user_command = SavedCommands(
            database_path=self.mock_database_path)
        # Arrange
        description = self.data_sample[0]
        command = self.data_sample[1]
        # Act
        # add a new command
        mock_user_command.add_new_command(
            command_description=description, new_command=command)
        # reopen the database
        mock_user_command_test = SavedCommands(
            database_path=self.mock_database_path)
        # and check if the row exists
        mock_user_command_test.cur.execute(
            "SELECT num_row, command_description, saved_command, "
            "date_created, timestamp_when_created, "
            "times_called, author_name, last_edited FROM saved_commands ORDER BY command_id")
        result = list(mock_user_command_test.cur.fetchall())
        # close the database
        mock_user_command_test.commit_and_close_database()
        date = None
        timestamp = None
        # edit the data sample timestamp
        for i in range(len(result)):
            if result[i][1] == self.data_sample[0]:
                timestamp = result[i][4]
                date = result[i][3]
                break
        t = self.data_sample
        new_data_sample = (t[0], t[1], date, timestamp, t[4], t[5], timestamp)
        # Add the element from the list to get the expected result
        expected_result = self.original_saved_commands_table
        expected_result.append(new_data_sample)
        # Add indexes to the table
        indexed_table = self.indexed_table(expected_result)
        # sort by element 0
        indexed_table.sort(key=lambda obj: obj[0])
        # Assert
        self.assertEqual(indexed_table, result)

    @staticmethod
    def table_of_three_indexed_elements(data_table):
        """
        Helper function that indexes elements from a list. Returns 3 element list.
        This is the format in which some tables are printed out in. Mocking the format here.
        Args:
            data_table: table to format.

        """
        # Create expected results table
        formatted_table = []
        t = data_table
        # for item in the table
        for i in range(len(t)):
            # Append custom_tag, description and saved command
            new_row = tuple([i + 1, t[i][0], t[i][1]])
            formatted_table.append(new_row)
        # and return the result table
        return formatted_table

    @staticmethod
    def indexed_table(data_table):
        """
        Helper function that indexes elements from a list. Returns 7 element list.
        This is the format in which some tables are printed out in. Mocking the format here.
        Args:
            data_table: table to format.

        """
        # Create expected results table
        formatted_table = []
        t = data_table
        for i in range(len(t)):
            # Appending custom_tag, description and saved command
            new_row = tuple([i + 1, t[i][0], t[i][1], t[i][2],
                            t[i][3], t[i][4], t[i][5], t[i][6]])
            formatted_table.append(new_row)
        # and return result table
        return formatted_table

    @staticmethod
    def table_of_three_elements(data_table):
        """
        Helper function that separates elements from a list. Returns 3 element list. These are NOT indexed.
        This is the format in which some tables are printed out in. Mocking the format here.
        Args:
            data_table: table to format.

        """
        # Create expected result table
        formatted_table = []
        t = data_table
        for i in range(len(t)):
            # Appending custom_tag, description and saved command
            new_row = tuple([t[i][0], t[i][1], t[i][2]])
            formatted_table.append(new_row)
        # and return resutl table
        return formatted_table

    def test_view_all_saved_commands(self):
        """
        Test if view all commands method returns the expected command list.

        """
        # Arrange
        # Create a mock command to work with
        mock_user_command = SavedCommands(
            database_path=self.mock_database_path)
        expected_result = self.table_of_three_indexed_elements(
            self.original_saved_commands_table)
        expected_result.sort()
        # Act
        # ask for the list of all saved commands
        result = mock_user_command.view_all_saved_commands()
        # Assert
        self.assertEqual(expected_result, result)

    @patch('command_saver.table.saved_commands.os.system')
    def test_execute_command(self, mock_os_system_call):
        """
        Tests execute_command and find_command methods of SavedCommands class.
        Args:
            mock_os_system_call: mock os call to execute the command. Just make sure it gets called.

        """
        # Arrange
        command_id = 1
        command_id_bad = 100
        # Create a mock commands to work with
        mock_user_command = SavedCommands(database_path=self.mock_database_path,
                                          command_id=command_id,
                                          )
        mock_user_command_bad = SavedCommands(database_path=self.mock_database_path,
                                              command_id=command_id_bad,
                                              )
        # Find expected result
        expected_result = self.original_saved_commands_table[0][1]
        expected_result_bad = ValueError
        # Act
        mock_user_command.execute_command()
        result_bad = mock_user_command_bad.execute_command()
        # Collect popularity data
        mock_command_two = SavedCommands(database_path=self.mock_database_path,
                                         command_id=command_id,
                                         )
        # And check if the row exists
        mock_command_two.cur.execute(
            "SELECT times_called FROM saved_commands WHERE num_row=?", (command_id,))
        # Fetch the record and format it
        result_increment = ''.join(map(str, mock_command_two.cur.fetchone()))
        # Assert
        mock_os_system_call.assert_called_once_with(expected_result)
        self.assertEqual(str(3), result_increment)
        self.assertEqual(expected_result_bad, result_bad)

    def test_update_command(self):
        """
        To test if update command works with good and bad input.

        """
        # Arrange
        command_id = 2
        command_id_bad = 100
        new_command = 'git -help'
        # create a mock command to work with
        mock_user_command = SavedCommands(database_path=self.mock_database_path,
                                          command_id=command_id)
        mock_user_command_bad = SavedCommands(database_path=self.mock_database_path,
                                              command_id=command_id_bad)
        # Act
        mock_user_command.update_command(new_command=new_command)
        mock_user_command_bad.update_command(new_command=new_command)
        result = mock_user_command.find_command()
        result_bad = sqlite3.Error
        # Assert
        self.assertEqual(new_command, result)
        self.assertEqual(result_bad, result_bad)

    @patch('command_saver.table.saved_commands.InputWindow')
    def test_edit_command(self, mock_input_window):
        """
        To test if edit command updates a command.
        Args:
            mock_input_window: mock user input.

        """
        # and a command to edit
        command_id = 1
        # pick value to change the command to
        change_value_to = 'git -help'
        # Arrange mock return values (sanity check & value)
        mock_input_window().ask_input.side_effect = ['y', change_value_to]
        # create a mock command to work with
        mock_user_command = SavedCommands(database_path=self.mock_database_path,
                                          command_id=command_id)
        # Act
        mock_user_command.edit_command()

        mock_user_command_result = SavedCommands(database_path=self.mock_database_path,
                                                 command_id=command_id)
        result = mock_user_command_result.find_command()
        # Assert
        self.assertEqual(change_value_to, result)

    def test_export_all(self):
        """
        To test if exportall command creates a file with correct contents.

        """
        # Arrange
        # Create a mock command to work with
        mock_user_command = SavedCommands(
            database_path=self.mock_database_path)
        mock_user_command_2 = SavedCommands(
            database_path=self.mock_database_path)
        # Act
        # Get expected contents
        expected_command_list = []
        # find all saved commands
        saved_command_output = mock_user_command.view_all_saved_commands()
        for line in saved_command_output:
            # join the content to match export format
            line = ', '.join(str(v) for v in line) + '\n'
            # append the line to the expected list
            expected_command_list.append(line)
        # Launch export command
        mock_user_command_2.export_all()
        # Read the file to get the result
        result = []
        with open(path.dirname(command_saver.__file__) + '/disposition/disposition.txt', 'r') as f:
            result = f.readlines()
        # Assert
        self.assertEqual(expected_command_list, result)
        # Remove the disposition file
        os.remove(path.dirname(command_saver.__file__) +
                  '/disposition/disposition.txt')

    def test_recent_commands_list(self):
        """
        To test if recent commands list returns an ordered list in the corect order.

        """
        # Arrange
        # Create a mock command to work with
        mock_user_command = SavedCommands(
            database_path=self.mock_database_path)
        # Find expected results
        expected_result = []
        data_table = self.indexed_table(self.original_saved_commands_table)
        # Find top 3 timestamps and add them to results
        data_table.sort(key=lambda obj: obj[4])
        # Only keep elements that are in the return statement of method
        data_table_of_four = self.table_of_three_elements(data_table)
        expected_result.extend(data_table_of_four[0:3])
        # Order all data by popularity
        data_table.sort(key=lambda obj: obj[6])
        # Only keep elements that are in the return statement of method
        data_table_of_four = self.table_of_three_elements(data_table)
        # Fetch top 8
        popular_data = data_table_of_four[0:9]
        # Add entities tha are not in the list already
        for i in range(len(popular_data)):
            if popular_data[i] in expected_result:
                continue
            else:
                expected_result.append(popular_data[i])
        # Act
        # Get the result data
        result = mock_user_command.recent_commands_list()
        # Assert
        self.assertEqual(expected_result, result)

    def test_find_command(self):
        """
        To test if find_command method finds entities it is supposed to,
        and rejects one's that are not in the database,

        """
        # Arrange
        command_id = 2
        command_id_bad = 100
        command_id_bad_2 = -10
        # create a mock commands to work with
        mock_user_command = SavedCommands(database_path=self.mock_database_path,
                                          command_id=command_id)
        mock_user_command_2 = SavedCommands(database_path=self.mock_database_path,
                                            command_id=command_id_bad)
        mock_user_command_3 = SavedCommands(database_path=self.mock_database_path,
                                            command_id=command_id_bad_2)
        # Find expected results
        expected_result = self.original_saved_commands_table[1][1]
        expected_result_2 = None
        expected_result_3 = None
        # Act
        # Get the result data
        result = mock_user_command.find_command()
        result_2 = mock_user_command_2.find_command()
        result_3 = mock_user_command_3.find_command()
        # Assert
        self.assertEqual(expected_result, result)
        self.assertEqual(expected_result_2, result_2)
        self.assertEqual(expected_result_3, result_3)


# this runs the test automatically
if __name__ == '__main__':
    unittest.main()
