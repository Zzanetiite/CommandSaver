import unittest
from command_saver.table.user_data import UserData
from unittest.mock import patch
from command_saver.utils.default_database import DefaultDatabase


class TestUserData(unittest.TestCase):
    mock_database_path = 'tests/data/command_saver.db'
    data_sample = ('hello', 'Say hello', '$echo Hello dearest world', 'date_today', 1234567890123, 0, 'admin')
    """
    Tests UserData class parameters and methods.
    """

    def setUp(self):
        """
        Create a test database before every test.

        """
        # create a mock database
        self.mock_database = DefaultDatabase(self.mock_database_path)
        self.mock_database.create_default_database()

    def tearDown(self):
        """
        Delete a test database after every unit test.
        Returns:

        """
        # delete mock database
        self.mock_database.delete_database()

    @patch('command_saver.table.user_data.sqlite3.connect')
    def test_parameters_exist(self, mock_connect_to_db):
        """
        Test whether parameters have been defined successfully.
        Test whether database is called when object is created.
        Args:
            mock_connect_to_db: mocks the sql connection to the database. Testing whether it is called.

        """
        # Arrange
        dummy_path = 'dummy_path.db'
        mock_object = UserData(database_path=dummy_path)
        # Assert
        self.assertEqual(dummy_path, mock_object.database)
        mock_connect_to_db.assert_called_once_with(dummy_path)

    def test_find_author(self):
        """
        Test whether finding author works.

        """
        # Arrange
        # create a mock command to work with
        mock_user_command = UserData(database_path=self.mock_database_path)
        # Act
        result_author = mock_user_command.find_author()
        # Assert
        self.assertEqual('admin', result_author)

    @patch('command_saver.table.user_data.InputWindow')
    def test_change_author(self, mock_input_window_author):
        """
        Test whether changing author method works.
        Args:
            mock_input_window_author: create a dummy response for the user input request.

        """
        # New author to set
        author = 'Somebody Else'
        # Arrange mock return value
        mock_input_window_author().ask_input.return_value = author
        # create a mock command to work with
        mock_user_command = UserData(database_path=self.mock_database_path)
        # Act
        # Change the author
        mock_user_command.change_author()
        # Make a new mock object to check if the action was done
        mock_user_command_result = UserData(database_path=self.mock_database_path)
        # Fetch data from database
        mock_user_command_result.cur.execute("SELECT username FROM user_data")
        # Format data
        result_list = ''.join(mock_user_command_result.cur.fetchone())
        # Assert
        self.assertEqual(author, result_list)

    @patch('command_saver.table.user_data.InputWindow')
    def test_change_authors_department(self, mock_input_window_author):
        """
        Test whether function to change author's department works.
        Args:
            mock_input_window_author: create a dummy response for the user input request.

        """
        # New author to set
        department = 'Software Development'
        # Arrange mock return value
        mock_input_window_author().ask_input.return_value = department
        # create a mock command to work with
        mock_user_command = UserData(database_path=self.mock_database_path)
        # Act
        # Change the author
        mock_user_command.change_authors_department()
        # Make a new mock object to check if the action was done
        mock_user_command_result = UserData(database_path=self.mock_database_path)
        # Fetch data from database
        mock_user_command_result.cur.execute("SELECT department FROM user_data")
        # Format data
        result_list = ''.join(mock_user_command_result.cur.fetchone())
        # Assert
        self.assertEqual(department, result_list)


# this runs the test automatically
if __name__ == '__main__':
    unittest.main()
