import unittest
from unittest.mock import patch
from command_saver.input_window.input_window import InputWindow


class TestInputWindow(unittest.TestCase):
    """
    Tests InputWindow class parameters and methods.
    """

    @patch('builtins.input', return_value='Yes')
    def test_ask_input_good(self, mock_input):
        """
        Test if ask input processes user input as expected when good answer is given
        Args:
            mock_input: mocks the response of a valid answer. When the method calls input, the value "Yes" is returned.

        """
        # Arrange
        msg = 'Test: '
        valid_answers = ['Yes']
        msg_info = 'Information.'
        # Act
        mock_object1 = InputWindow().ask_input(
            msg=msg,
            valid_answers=valid_answers,
            msg_info=msg_info,
        )
        # Assert
        self.assertEqual(valid_answers[0], mock_object1)

    @patch('builtins.input', side_effect=['No', 'Yes', '012', 'b'])
    def test_ask_input_varies(self, mock_input):
        """
        Test if ask input processes user input as expected when varying answers are given.
        Args:
            mock_input: mocks input() function responses in given order.

        """
        # Arrange
        msg = 'Test: '
        valid_answers = ['Yes']
        msg_info = 'Information.'
        # Act - call the function with different side effects
        mock_object1 = InputWindow().ask_input(
            msg=msg,
            valid_answers=valid_answers,
            msg_info=msg_info,
        )
        mock_object2 = InputWindow().ask_input(
            msg=msg,
            valid_answers=valid_answers,
            msg_info=msg_info,
        )
        # Assert
        self.assertEqual(valid_answers[0], mock_object1)
        self.assertEqual('b', mock_object2)
        self.assertEqual(mock_input.call_count, 4)


# this runs the test automatically
if __name__ == '__main__':
    unittest.main()
