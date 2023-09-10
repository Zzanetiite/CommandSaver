import unittest
from command_saver.run_me import RunMe
from unittest.mock import patch, MagicMock, PropertyMock


class TestRunMe(unittest.TestCase):
    """
    Tests RunMe class methods.
    """
    # create options for testing
    valid_menu_options = ['e', 'a', 'edit', 'd', 'b', 'ss', 'bs', 'help', 'r', 'q', 'exportall', 'setuser', 'setuserdep']

    @patch('command_saver.run_me.RunMe.valid_ids', new_callable=PropertyMock)
    def test_convert_answer(self, mock_ids):
        """
        To test convert answer method. Are answers converted as expected? This is supposed to be
        relatively user-friendly: it takes input and separates it even when user has made same mistakes,
        like extra spaces, extra text.
        Args:
            mock_ids: patch valid_ids. These will not be created at this stage by the program,
            so the list will be empty.

        """
        # Arrange
        # give valid_ids some return values
        mock_ids.return_value = [2, 3, 1]
        # Some use cases to test
        answer = 'exportall   2'
        answer2 = 'a3'
        answer3 = 'sfsf    1002'
        answer4 = 'bs 1'
        answer5 = 'setuserdep'
        answer6 = '-100setuserdep'
        answer7 = 'b'
        # Act
        # Find results
        r_option, r_command_id = RunMe().convert_answer(answer)
        r_option2, r_command_id2 = RunMe().convert_answer(answer2)
        r_option3, r_command_id3 = RunMe().convert_answer(answer3)
        r_option4, r_command_id4 = RunMe().convert_answer(answer4)
        r_option5, r_command_id5 = RunMe().convert_answer(answer5)
        r_option6, r_command_id6 = RunMe().convert_answer(answer6)
        r_option7, r_command_id7 = RunMe().convert_answer(answer7)
        # Assert
        self.assertEqual(r_option, 'exportall')
        self.assertEqual(r_command_id, 2)
        self.assertEqual(r_option2, 'a')
        self.assertEqual(r_command_id2, 3)
        self.assertEqual(r_option3, 'sfsf')
        self.assertEqual(r_command_id3, None)
        self.assertEqual(r_option4, 'bs')
        self.assertEqual(r_command_id4, 1)
        self.assertEqual(r_option5, 'setuserdep')
        self.assertEqual(r_command_id5, None)
        self.assertEqual(r_option6, None)
        self.assertEqual(r_command_id6, None)
        self.assertEqual(r_option7, 'b')
        self.assertEqual(r_command_id7, None)

    @patch('command_saver.run_me.ViewContents')
    @patch('command_saver.run_me.InputWindow')
    def test_quit(self, mock_input_window, mock_view_contents):
        """
        To test if quit works for the main menu.
        Args:
            mock_input_window: mock user input.
            mock_view_contents: mock menus.

        """
        """
        First test to check if the test will leave the while loop when expected.
        """
        # Arrange mock return values
        mock_view_contents().print_main_menu = MagicMock()
        mock_input_window().ask_input.side_effect = ['q']
        # Act
        return_string = RunMe().run_program()
        # Assert
        self.assertTrue(mock_view_contents().print_main_menu.called_once)
        self.assertTrue(mock_input_window().ask_input.called_once)
        self.assertEqual('CommandSaver program exited.', return_string)

    @patch('command_saver.run_me.RunMe.valid_options', new_callable=PropertyMock)
    @patch('command_saver.run_me.ViewContents')
    @patch('command_saver.run_me.InputWindow')
    def test_None_and_b(self, mock_input_window, mock_view_contents, mock_valid_options):
        """
        Test if no option is provided will return the program back to main menu.
        Args:
            mock_input_window: mock user input.
            mock_view_contents: mock menus.
            mock_valid_options: patch valid_options. These will not be created at this stage by the program,
            so the list will be empty.

        """
        # Arrange mock return values
        mock_view_contents().print_main_menu = MagicMock()
        mock_input_window().ask_input.side_effect = ['-10invalid_string', 'bad inpietpefjsfdv -231243', '___', '   ',
                                                     'bs', 'b', 'q']
        # give valid_options return values
        mock_valid_options.return_value = self.valid_menu_options
        # Act
        return_string = RunMe().run_program()
        # Assert
        self.assertTrue(mock_input_window().ask_input.call_count, 6)
        self.assertEqual(mock_view_contents().print_main_menu.call_count, 5)
        self.assertEqual('CommandSaver program exited.', return_string)

    # Patch valid options. These will not be created at this stage by the program, so the list will be empty.
    @patch('command_saver.run_me.RunMe.valid_options', new_callable=PropertyMock)
    @patch('command_saver.run_me.ViewContents')
    @patch('command_saver.run_me.InputWindow')
    def test_bs_and_help(self, mock_input_window, mock_view_contents, mock_valid_options):
        """
        Test if go back to saved commands menu and help page works.
        Args:
            mock_input_window: to mock user input.
            mock_view_contents: to mock menus.
            mock_valid_options: to patch menu_options. These will not be created at this stage by the program,
            so the list will be empty.

        """
        # Arrange mock return values
        mock_view_contents().print_main_menu = MagicMock()
        mock_input_window().ask_input.side_effect = ['bs', 'help', 'q']
        mock_view_contents().print_saved_commands_menu = MagicMock()
        mock_view_contents().print_help_page = MagicMock()
        # give valid_options return values
        mock_valid_options.return_value = self.valid_menu_options
        # Act
        return_string = RunMe().run_program()
        # Assert
        self.assertEqual(mock_view_contents().print_main_menu.call_count, 1)
        self.assertTrue(mock_input_window().ask_input.call_count, 3)
        self.assertEqual('CommandSaver program exited.', return_string)
        self.assertEqual(mock_view_contents().print_help_page.call_count, 1)
        self.assertEqual(mock_view_contents().print_saved_commands_menu.call_count, 1)

    @patch('command_saver.run_me.RunMe.valid_options', new_callable=PropertyMock)
    @patch('command_saver.run_me.ViewContents')
    @patch('command_saver.run_me.InputWindow')
    @patch('command_saver.run_me.UserData')
    def test_user_data(self, mock_user_data, mock_input_window, mock_view_contents, mock_valid_options):
        """
        Test if user data change is called.
        Args:
            mock_user_data: mock UserData method, it is already tested in user_table tests.
            mock_input_window: mock user input.
            mock_view_contents: mock menus.
            mock_valid_options: patch valid_ids. These will not be created at this stage by the program,
            so the list will be empty.

        """
        # Arrange mock return values
        mock_view_contents().print_main_menu = MagicMock()
        mock_input_window().ask_input.side_effect = ['setuser', 'setuserdep', 'q']
        mock_user_data().change_author = MagicMock()
        mock_user_data().change_authors_department = MagicMock()
        # give valid_options return values
        mock_valid_options.return_value = self.valid_menu_options
        # Act
        return_string = RunMe().run_program()
        # Assert
        self.assertEqual(mock_view_contents().print_main_menu.call_count, 1)
        self.assertEqual(mock_user_data().change_author.call_count, 1)
        self.assertEqual(mock_user_data().change_authors_department.call_count, 1)
        self.assertTrue(mock_input_window().ask_input.call_count, 3)
        self.assertEqual('CommandSaver program exited.', return_string)

    @patch('command_saver.run_me.RunMe.valid_options', new_callable=PropertyMock)
    @patch('command_saver.run_me.ViewContents')
    @patch('command_saver.run_me.InputWindow')
    @patch('command_saver.run_me.SavedCommands')
    def test_execute(self, mock_saved_commands, mock_input_window, mock_view_contents,
                     mock_valid_options):
        """
        Test if execute command gets called when it is supposed to.
        Test if all use cases work as expected
        Args:
            mock_saved_commands: mock SavedCommands class, it is tested under saved_commands tests.
            mock_input_window: mock user input.
            mock_view_contents: mock menus.
            mock_valid_options: patch menu_options. These will not be created at this stage by the program,
            so the list will be empty.

        """
        # Arrange mock return values
        mock_view_contents().print_main_menu = MagicMock()
        mock_input_window().ask_input.side_effect = ['e', '1', 'e 2', 'q']
        mock_saved_commands().execute_command.return_value = None
        # give valid_options return values
        mock_valid_options.return_value = self.valid_menu_options
        # Act
        return_string = RunMe().run_program()
        # Assert
        self.assertEqual(mock_view_contents().print_main_menu.call_count, 1)
        self.assertEqual(mock_input_window().ask_input.call_count, 4)
        self.assertTrue(mock_saved_commands().execute_command.call_count, 2)
        self.assertEqual('CommandSaver program exited.', return_string)

    @patch('command_saver.run_me.RunMe.valid_options', new_callable=PropertyMock)
    @patch('command_saver.run_me.ViewContents')
    @patch('command_saver.run_me.InputWindow')
    @patch('command_saver.run_me.SavedCommands')
    def test_delete(self, mock_saved_commands, mock_input_window, mock_view_contents, mock_valid_options):
        """
        Test if delete command gets called when it is supposed to.
        Test if all use cases work as expected
        Args:
            mock_saved_commands: mock SavedCommands class, it is tested under saved_commands tests.
            mock_input_window: mock user input.
            mock_view_contents: mock menus.
            mock_valid_options: patch menu_options. These will not be created at this stage by the program,
            so the list will be empty.

        """
        # Arrange mock return values
        mock_view_contents().print_main_menu = MagicMock()
        mock_input_window().ask_input.side_effect = ['d', '1', 'd 2', 'q']
        mock_saved_commands().delete_command = MagicMock()
        mock_view_contents().print_intermediate_menu = MagicMock()
        # give valid_options return values
        mock_valid_options.return_value = self.valid_menu_options
        # Act
        return_string = RunMe().run_program()
        # Assert
        self.assertEqual(mock_view_contents().print_main_menu.call_count, 1)
        self.assertEqual(mock_input_window().ask_input.call_count, 4)
        self.assertTrue(mock_saved_commands().delete_command.call_count, 2)
        self.assertTrue(mock_view_contents().print_intermediate_menu.call_count, 1)
        self.assertEqual('CommandSaver program exited.', return_string)

    @patch('command_saver.run_me.RunMe.valid_options', new_callable=PropertyMock)
    @patch('command_saver.run_me.ViewContents')
    @patch('command_saver.run_me.InputWindow')
    @patch('command_saver.run_me.SavedCommands')
    def test_edit(self, mock_saved_commands, mock_input_window, mock_view_contents, mock_valid_options):
        """
        Test if edit command gets called when it is supposed to.
        Test if all use cases work as expected
        Args:
            mock_saved_commands: mock SavedCommands class, it is tested under saved_commands tests.
            mock_input_window: mock user input.
            mock_view_contents: mock menus.
            mock_valid_options: patch menu_options. These will not be created at this stage by the program,
            so the list will be empty.

        """
        # Arrange mock return values
        mock_view_contents().print_main_menu = MagicMock()
        mock_input_window().ask_input.side_effect = ['edit', '1', 'edit 2', 'q']
        mock_saved_commands().edit_command = MagicMock()
        mock_view_contents().print_intermediate_menu = MagicMock()
        # give valid_options return values
        mock_valid_options.return_value = self.valid_menu_options
        # Act
        return_string = RunMe().run_program()
        # Assert
        self.assertEqual(mock_view_contents().print_main_menu.call_count, 1)
        self.assertEqual(mock_input_window().ask_input.call_count, 4)
        self.assertTrue(mock_saved_commands().edit_command.call_count, 2)
        self.assertTrue(mock_view_contents().print_intermediate_menu.call_count, 1)
        self.assertEqual('CommandSaver program exited.', return_string)

    @patch('command_saver.run_me.RunMe.valid_options', new_callable=PropertyMock)
    @patch('command_saver.run_me.ViewContents')
    @patch('command_saver.run_me.InputWindow')
    @patch('command_saver.run_me.SavedCommands')
    def test_add(self, mock_saved_commands, mock_input_window, mock_view_contents, mock_valid_options):
        """
        Test if addd command gets called when it is supposed to.
        Test if all use cases work as expected
        Args:
            mock_saved_commands: mock SavedCommands class, it is tested under saved_commands tests.
            mock_input_window: mock user input.
            mock_view_contents: mock menus.
            mock_valid_options: patch menu_options. These will not be created at this stage by the program,
            so the list will be empty.
        """
        # Arrange mock return values
        mock_view_contents().print_main_menu = MagicMock()
        mock_input_window().ask_input.side_effect = ['a', 'description', 'terminal command', 'q']
        mock_saved_commands().add_new_command = MagicMock()
        mock_view_contents().print_intermediate_menu = MagicMock()
        # give valid_options return values
        mock_valid_options.return_value = self.valid_menu_options
        # Act
        return_string = RunMe().run_program()
        # Assert
        self.assertEqual(mock_view_contents().print_main_menu.call_count, 1)
        self.assertEqual(mock_input_window().ask_input.call_count, 4)
        self.assertTrue(mock_saved_commands().add_new_command.call_count, 1)
        self.assertTrue(mock_view_contents().print_intermediate_menu.call_count, 1)
        self.assertEqual('CommandSaver program exited.', return_string)

    @patch('command_saver.run_me.RunMe.valid_options', new_callable=PropertyMock)
    @patch('command_saver.run_me.ViewContents')
    @patch('command_saver.run_me.InputWindow')
    @patch('command_saver.run_me.SavedCommands')
    def test_exportall(self, mock_saved_commands, mock_input_window, mock_view_contents, mock_valid_options):
        """
        Test if exportall command gets called when it is supposed to.
        Test if all use cases work as expected
        Args:
            mock_saved_commands: mock SavedCommands class, it is tested under saved_commands tests.
            mock_input_window: mock user input.
            mock_view_contents: mock menus.
            mock_valid_options: patch menu_options. These will not be created at this stage by the program,
            so the list will be empty.
        """
        # Arrange mock return values
        mock_view_contents().print_main_menu = MagicMock()
        mock_input_window().ask_input.side_effect = ['exportall',
                                                     'exportall 23235 I made mistakes writing this, but it should work',
                                                     'q']
        mock_saved_commands().export_all = MagicMock()
        # give valid_options return values
        mock_valid_options.return_value = self.valid_menu_options
        # Act
        return_string = RunMe().run_program()
        # Assert
        self.assertEqual(mock_view_contents().print_main_menu.call_count, 1)
        self.assertEqual(mock_input_window().ask_input.call_count, 3)
        self.assertTrue(mock_saved_commands().export_all.call_count, 2)
        self.assertEqual('CommandSaver program exited.', return_string)

    @patch('command_saver.run_me.RunMe.valid_options', new_callable=PropertyMock)
    @patch('command_saver.run_me.ViewContents')
    @patch('command_saver.run_me.InputWindow')
    @patch('command_saver.run_me.SavedCommands')
    @patch('command_saver.run_me.UserData')
    def test_repeat(self, mock_user_data, mock_saved_commands, mock_input_window,
                    mock_view_contents, mock_valid_options):
        """
        Test if repeat is called for options it is available for.
        Args:
            mock_saved_commands: mock SavedCommands class, it is tested under saved_commands tests.
            mock_input_window: mock user input.
            mock_view_contents: mock menus.
            mock_valid_options: patch menu_options. These will not be created at this stage by the program,
            so the list will be empty.
        """
        # Arrange mock return values
        mock_view_contents().print_main_menu = MagicMock()
        mock_input_window().ask_input.side_effect = ['a 2', 'r', 'r',
                                                     'setuser', 'r',
                                                     'setuserdep', 'r',
                                                     'e 1', 'r', '2',
                                                     'edit 2', 'r', '1',
                                                     'd 1', 'r', '2',
                                                     'q']
        mock_saved_commands().add_new_command = MagicMock()
        mock_view_contents().print_intermediate_menu = MagicMock()
        mock_user_data().change_author = MagicMock()
        mock_user_data().change_authors_department = MagicMock()
        mock_saved_commands().execute_command.return_value = None
        mock_saved_commands().delete_command = MagicMock()
        mock_saved_commands().edit_command = MagicMock()
        # give valid_options return values
        mock_valid_options.return_value = self.valid_menu_options
        # Act
        return_string = RunMe().run_program()
        # Assert
        self.assertEqual(mock_view_contents().print_main_menu.call_count, 4)
        self.assertEqual(mock_input_window().ask_input.call_count, 17)
        self.assertTrue(mock_saved_commands().add_new_command.call_count, 2)
        self.assertEqual(mock_user_data().change_author.call_count, 2)
        self.assertEqual(mock_user_data().change_authors_department.call_count, 2)
        self.assertTrue(mock_saved_commands().execute_command.call_count, 2)
        self.assertTrue(mock_saved_commands().delete_command.call_count, 2)
        self.assertTrue(mock_saved_commands().edit_command.call_count, 2)
        self.assertTrue(mock_view_contents().print_intermediate_menu.call_count, 3)
        self.assertEqual('CommandSaver program exited.', return_string)


# this runs the test automatically
if __name__ == '__main__':
    unittest.main()