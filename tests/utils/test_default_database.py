import unittest
from unittest.mock import patch, MagicMock
from command_saver.utils.default_database import DefaultDatabase
from os.path import exists
from os import path
import sqlite3
import command_saver


class TestDefaultDatabase(unittest.TestCase):
    mock_database_path = 'tests/data/command_saver.db'
    """
    Tests CreateDefaultDatabase parameters and methods.
    """

    def setUp(self):
        """
        Create a test database and expected results to use for testing.

        """
        # Create an object of the default database
        # (this does not create a database, only object)
        self.mock_object = DefaultDatabase()
        # Create an object of the database used for testing
        self.mock_object_for_tests = DefaultDatabase(mock_database_path=self.mock_database_path)
        # Create the testing database for each test
        self.mock_object_for_tests.create_default_database()
        # Create a list with current data
        self.expected_saved_commands_data = [
            ('Check git status', 'git status', str(self.mock_object.date_today),
             int(self.mock_object.timestamp_now * 1000), 2, 'admin', int(self.mock_object.timestamp_now * 1000)),
            ('Add all git command', 'git add --all', str(self.mock_object.date_today),
             int(self.mock_object.timestamp_now * 1000), 0, 'admin', int(self.mock_object.timestamp_now * 1000)),
            ('Go 4 folders out', 'cd ../../../..', str(self.mock_object.date_today),
             int(self.mock_object.timestamp_now * 1000), 4, 'admin', int(self.mock_object.timestamp_now * 1000)),
            ('Hello world!', '$echo "Hello world!"', str(self.mock_object.date_today),
             int(self.mock_object.timestamp_now * 1000), 5, 'admin', int(self.mock_object.timestamp_now * 1000)),
        ]

    def tearDown(self):
        """
        Delete the test database after every unit test.

        """
        # Delete the test database
        self.mock_object_for_tests.delete_database()

    def test_parameters_exist(self):
        """
        Test whether parameters have been defined successfully and correctly.
        """
        # Assert parameters are as expected
        self.assertEqual(None, self.mock_object.existing_data)
        self.assertEqual(None, self.mock_object.existing_data_path)
        self.assertEqual(None, self.mock_object.mock_database_path)
        self.assertEqual(path.dirname(command_saver.__file__) + '/data/command_saver.db', self.mock_object.database_path)
        self.assertEqual(self.mock_database_path, self.mock_object_for_tests.database_path)
        self.assertTrue(exists(self.mock_database_path))
        self.assertEqual('admin', self.mock_object.author)
        self.assertEqual(self.expected_saved_commands_data, self.mock_object.saved_commands_data)

    @patch('command_saver.utils.default_database.remove')
    def test_delete_database(self, mock_remove):
        """
        Test whether delete database method calls the os delete module.
        Args:
            mock_remove: mocks the remove module.

        """
        # Act
        # Try to delete command with patched remove
        self.mock_object_for_tests.delete_database()
        # Assert remove was called
        mock_remove.assert_called_once()

    def test_keep_backup_mock_db(self):
        """
        To test whether keep backup will return False for mock databases (like this test).
        This is to allow for easier testing, because default database is used for all database table testing.

        """
        # Act
        result_when_testing = self.mock_object_for_tests.keep_backup()
        # Assert
        self.assertEqual(False, result_when_testing)

    @patch('command_saver.utils.default_database.Path')
    @patch('command_saver.utils.default_database.InputWindow')
    @patch('command_saver.utils.default_database.remove')
    def test_keep_backup_true_delete_yes(self, mock_remove, mock_input_window, mock_pathlib):
        """
        To test use case of keep_backup method when the response is Yes, delete it.
        Args:
            mock_remove: mocks database removal.
            mock_input_window: mocks user response for the question: keep backup?
            mock_pathlib: mocks file existence check. True =  file exists,

        """
        # Arrange mock return values
        mock_pathlib.is_file().side_effect = [True, True]
        mock_input_window().ask_input.side_effect = ['Yes', 'Y']
        # Act
        result = self.mock_object.keep_backup()
        # Assert
        self.assertEqual(False, result)
        mock_input_window().ask_input.assert_called_once()
        mock_pathlib.assert_called_once()
        mock_remove.assert_called_once()

    @patch('command_saver.utils.default_database.Path')
    @patch('command_saver.utils.default_database.InputWindow')
    def test_keep_backup_true_delete_No(self, mock_input_window, mock_pathlib):
        """
        To test use case of keep_backup method when the response is No, doo't delete it.
        Args:
            mock_input_window: mocks user response for the question: keep backup?
            mock_pathlib: mocks file existence check. True =  file exists,

        """
        # Arrange mock return values
        mock_pathlib.return_value.is_file.side_effect = [True, True]
        mock_input_window().ask_input.side_effect = ['No', 'N']
        # Act
        result = self.mock_object.keep_backup()
        # Assert
        self.assertEqual(True, result)
        mock_input_window().ask_input.assert_called_once()
        mock_pathlib.assert_called_once()

    @patch('command_saver.utils.default_database.Path')
    def test_keep_backup_false(self, mock_pathlib):
        """
        To test use case of keep_backup method when the database does not exist already.
        Args:
            mock_pathlib: mocks file existence check. False =  file does not exist,

        """
        # Arrange mock return values
        mock_pathlib.return_value.is_file.return_value = False
        # Act
        result = self.mock_object.keep_backup()
        # Assert
        self.assertEqual(False, result)
        mock_pathlib.assert_called_once()

    @patch.object(DefaultDatabase, 'keep_backup', new_callable=MagicMock)
    def test_create_default_database_keep_backup(self, mock_keep_backup):
        """
        To test create default database function when use chose
        to keep the backup and stop the database reset.
        Args:
            mock_keep_backup: mock the user response for the keep backup method. Keep backup? True (yes)

        """
        # Arrange mock return value for keep backup method
        mock_keep_backup.return_value = True
        # Act
        result = self.mock_object_for_tests.create_default_database()
        # Assert
        self.assertEqual(
            "Database exists. The command cancelled and a new database not created. "
            "\nDatabase location: tests/data/command_saver.db",
            result)

    def test_create_default_database(self):
        """
        Test whether a default database creates when calling the create database method.

        """
        # Arrange
        # Open connection with SQL
        con = sqlite3.connect(self.mock_database_path)
        # Allows to navigate in SQL
        cur = con.cursor()
        # Act
        # Read data from databases
        cur.execute(
            "SELECT command_description, saved_command, "
            "date_created, timestamp_when_created, "
            "times_called, author_name, last_edited FROM saved_commands ORDER BY command_id")
        result_saved_commands = (list(cur.fetchall()))
        cur.execute("SELECT option_tag, option_description, timestamp_when_created  FROM menu_options")
        result_menu_options = (list(cur.fetchall()))
        cur.execute("SELECT username FROM user_data")
        result_username = ''.join(cur.fetchone())
        # Assert
        self.assertEqual(self.expected_saved_commands_data, result_saved_commands)
        self.assertEqual(self.mock_object_for_tests.menu_options_data, result_menu_options)
        self.assertEqual('admin', result_username)


# this runs the test automatically
if __name__ == '__main__':
    unittest.main()
