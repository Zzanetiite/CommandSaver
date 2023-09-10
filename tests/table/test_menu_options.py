import unittest
from unittest.mock import patch
from command_saver.utils.default_database import DefaultDatabase
from command_saver.table.menu_options import MenuOptions


class TestMenuOptions(unittest.TestCase):
    mock_database_path = 'tests/data/command_saver.db'
    """
    Tests MenuOptions class parameters and methods.
    """

    def setUp(self):
        """
        Set up mock databases to test in the unit tests.

        """
        # create a mock database
        self.mock_database = DefaultDatabase(self.mock_database_path)
        self.mock_database.create_default_database()
        self.original_menu_table = self.mock_database.menu_options_data

    def tearDown(self):
        """
        Delete the test database after each test.

        """
        # delete mock database
        self.mock_database.delete_database()

    @patch('command_saver.table.user_data.sqlite3.connect')
    def test_parameters_exist(self, mock_connect_to_db):
        """
        Test whether parameters have been defined successfully.
        Test whether database is called when object is created.
        """
        # Arrange
        dummy_path = 'dummy_path.db'
        mock_object = MenuOptions(database_path=dummy_path)
        # Assert
        self.assertEqual(dummy_path, mock_object.database)
        mock_connect_to_db.assert_called_once_with(dummy_path)

    @staticmethod
    def numbered_table_of_three(data_table):
        """
        Takes a table, keeps first two values, assigns indexes as element 0.
        Args:
            data_table: table to arrange.

        Returns: arranged table.

        """
        # Create expected result table
        expected_result = []
        t = data_table
        for i in range(len(t)):
            # Appending custom_tag, description and saved command
            new_row = tuple([i + 1, t[i][0], t[i][1]])
            expected_result.append(new_row)
        return expected_result

    def test_view_options(self):
        """
        Test whether returned table is the table in the database.

        """
        # Arrange
        # Create a mock command to work with
        mock_user_command = MenuOptions(database_path=self.mock_database_path)
        expected_result = self.numbered_table_of_three(self.original_menu_table)
        expected_result.sort()
        # Act
        # ask for the list of all saved commands
        result = mock_user_command.view_options()
        # Assert
        self.assertEqual(expected_result, result)


# this runs the test automatically
if __name__ == '__main__':
    unittest.main()
