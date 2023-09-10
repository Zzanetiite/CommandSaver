from typing import Union, List


class InputWindow:
    """
    Class that takes user input.
    """
    def ask_input(self,
                  msg: str,
                  valid_answers: Union[str, list, tuple],
                  msg_info: str = None,
                  is_input_from_args: bool = False,
                  input_from_args: str = None,
                  ):
        """
        Asks user input, checks it, validates it and returns good input.
        Args:
            msg: message for the input request.
            msg_info: message information statement, printed before the msg.
            valid_answers: answers that are accepted as input or "any_string" for any answer.
        """
        # If there are instructions
        if msg_info is not None:
            # Print information/instructions
            print(msg_info)
        # Take user input
        if is_input_from_args:
            user_input = input_from_args
        else:
            user_input = input(msg, )
        # Check the input and return the result
        input_ok, user_input = self.__is_the_answer_valid(valid_answers=valid_answers, answer=user_input)
        # Ask for input while we are at this question or good answer is given.
        while input_ok is not True:
            # Check if user wants to leave
            if input_ok is None:
                # if so, return None to the outer function
                return user_input
            # If not True or None it is False
            else:
                # Print what happened
                print(f'Sorry! {user_input} is not a valid answer. Please try again or exit.')
                # Print valid answers
                if valid_answers == 'any_string':
                    valid_print_text = 'any text.'
                else:
                    valid_print_text = ', '.join(str(x) for x in valid_answers)
                print(f"Valid answers: {valid_print_text}")
                if msg_info is not None:
                    # Print information/instructions
                    print(msg_info)
                # Take user input
                user_input = input(msg, )
                # Check the input and return the result
                input_ok, user_input = self.__is_the_answer_valid(valid_answers=valid_answers, answer=user_input)
                continue
        # If the loop has broken, an answer has been given.
        return user_input

    @staticmethod
    def __is_the_answer_valid(valid_answers: Union[str, List[str]], answer):
        """Checks the answer and returns whether it is valid and the answer itself."""
        # try to turn the input into integer
        try:
            answer = int(answer)
        # except when it is not an integer
        except ValueError:
            pass
        # If answer is a menu option available anywhere in the program, return it.
        # These are: quit, Main Menu, saved commands menu
        if answer in ['q', 'b', 'bs']:
            # None stands for: No answer chosen, user chose to leave.
            return None, answer
        # If allowed input is any string,
        elif valid_answers == 'any_string':
            # if it is a global command
            if answer in ['q', 'b', 'bs']:
                # return it
                return None, answer
            # otherwise
            else:
                # make sure it is a string
                str_answer = str(answer)
                # and return True and the answer
                return True, str_answer
        # If the answer is in the valid answers
        elif answer in valid_answers:
            # it is valid, so return True and the answer
            return True, answer
        # If not in the valid answers
        else:
            # The answer is not valid and it is returned
            return False, str(answer)



