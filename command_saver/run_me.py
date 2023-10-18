import sqlite3
import argparse

from command_saver.visual_design.view_contents import ViewContents
from command_saver.input_window.input_window import InputWindow
from command_saver.visual_design.formatter import StringFormatter
from command_saver.table.saved_commands import SavedCommands
from command_saver.table.user_data import UserData
from command_saver.utils.default_database import DefaultDatabase
import re
from pathlib import Path
from command_saver.constants import (
    database_path,
    mo_a,
    mo_d,
    mo_e,
    mo_edit,
    mo_ss,
    mo_t,
    mo_mm,
    mo_scm,
    mo_help,
    mo_r,
    mo_q,
    mo_exp,
    mo_username,
    mo_userdep,
    global_commands
)


class RunMe:
    """
    Manages the running of the CommandSaver program. Call run_program() to run it.
    """
    valid_options = []
    valid_ids = []
    # Prepare variables for the user's choice of option and command_id
    option = None
    command_id = None
    # Prepare last_command variable to track last command used by user
    last_command = None
    # Prepare a variable to allow user to repeat the same command multiple times
    repeat_last_command = False
    # Check if database exists before doing anything else
    # Load database path used in the program
    database = database_path
    # If path exists
    if Path(database).is_file():
        # Pass and do nothing
        pass
    # If path does not exist
    else:
        # Create a new default database and let the user know it was done
        DefaultDatabase().create_default_database()
    # Track one-time commands (straight into terminal using args)
    one_action_only = False
    one_action_only_executed = False

    def __init__(self, args=None):
        # Allows to call the options and commands from terminal without opening the program
        self.args = args
        self.parser = argparse.ArgumentParser(
            description="Your program description here")
        self.parser.add_argument('option', nargs="?", default=None,
                                 help="Use e to execute a saved command")
        self.parser.add_argument("command_id", nargs="?", default=None,
                                 help="Specify the Command ID (number) of the command")

        # If submitted as terminal call for a single execute
        args = self.parser.parse_args()
        args_option = args.option
        args_command_id = args.command_id

        # If executing an existing command
        if args_option:
            # Check for it and assign them
            if args_command_id:
                self.option = args_option
                self.command_id = args_command_id
                self.one_action_only = True
            # Or just assign the option (this is validated in the main)
            else:
                self.option = args_option
                self.one_action_only = True

    def __refresh_lists(self):
        """
        Refreshes lists of valid menu options and command ids.
        Returns: updated class variables.

        """
        # Use menu options list of the program to get values
        t = ViewContents().menu_options_list
        # for index in the menu list of tuples
        for i in range(len(t)):
            # add each menu option to valid_options
            self.valid_options.append(t[i][1])
        # from existing saved commands list
        t2 = ViewContents().all_saved_commands_list
        # for index in the saved commands list of tuples
        for i in range(len(t2)):
            # add the command_id to the valid_ids list
            self.valid_ids.append(t2[i][0])

    def run_program(self):
        """
        Runs CommandSaver program by calling all needed modules.
        Returns: running program in the terminal.

        """
        if self.option == None:
            # Launch the main menu to ask user what they want to do
            ViewContents().print_main_menu()
        #  While not exiting the program
        while self.option != mo_q.key:
            # refresh lists
            self.__refresh_lists()
            # Check if the command is a repetition of the previous command
            if self.repeat_last_command:
                # If it is, change to false. Not all commands can be repeated.
                # This is triggered by commands that allow repetition or
                # to launch an option at a specific point.
                self.repeat_last_command = False
            # If not a repeated command,
            else:
                # If anything but single action
                if not self.one_action_only:
                    # If needed one action only, quit the program
                    if self.one_action_only_executed:
                        self.option = mo_q.key
                    else:
                        # Ask what the user would like to do next.
                        self.option, self.command_id = self.convert_answer((InputWindow().ask_input(
                            msg='\nPlease choose what you would like to do: ',
                            valid_answers='any_string')))
                # If single action, make it 0 and set the execution flag to true
                else:
                    self.one_action_only -= 1
                    self.one_action_only_executed = True
                    self.option, self.command_id = self.convert_answer((InputWindow().ask_input(
                        msg='\nValidating input...',
                        valid_answers='any_string',
                        is_input_from_args=True,
                        input_from_args=self.option + str(self.command_id) if self.command_id is not None else self.option)))
            # If answer for option is None, there was an error,
            # go back to Main Menu to remind user of options available.
            # Main Menu.
            if self.option == mo_mm.key:
                # Print the Main Menu
                ViewContents().print_main_menu()
                # Go back to the start of the loop
                continue
            if self.option is None:
                continue
            # If menu option is not one of the valid menu options,
            if self.option not in self.valid_options:
                # Let the user know that error has occurred because option was not found.
                StringFormatter(
                    text_to_format='Error! Option not in the Main Menu.').print_red_bold()
                # ask them to try again
                print('Please try again.')
                # and return to the start of the loop
                continue
            # Saved Commands Menu
            if self.option == mo_scm.key:
                # Print the Saved Commands Menu
                ViewContents().print_saved_commands_menu()
                # and return to the start of the loop
                continue
            # Help page
            if self.option == mo_help.key:
                # Print Help Page
                ViewContents().print_help_page()
                # and return to the start of the loop
                continue
            # If option to set username is chosen
            if self.option == mo_username.key:
                # Use option setuser and keep note whether error occurred
                option_stopped = self.do_repeatable_menu_option(error=sqlite3.Error,
                                                                menu_option=self.__option_to_setuser)
                # If error happened
                if option_stopped:
                    # Go back to the start of the loop
                    continue
            # If option to set user's department is chosen
            if self.option == mo_userdep.key:
                # Use option setuserdep and keep note whether error occurred
                option_stopped = self.do_repeatable_menu_option(error=sqlite3.Error,
                                                                menu_option=self.__option_to_setuserdep)
                # If error happened
                if option_stopped:
                    # Go back to the start of the loop
                    continue
            # If chosen option is to execute text into terminal
            if self.option == mo_t.key:
                if self.command_id is None:
                    self.command_id = InputWindow().ask_input(
                        msg='Terminal text not found. Please enter text: ',
                        valid_answers="any_string")
                # If provided id is not and id but a request of an option
                global_cmd = self.__global_option_checker(self.command_id)
                if global_cmd:
                    continue
                # Use option execute function and keep note whether error occurred
                option_stopped = self.do_repeatable_menu_option(error=ValueError,
                                                                menu_option=self.__option_to_execute_text_in_terminal)
                # If error happened
                if option_stopped:
                    # Go back to the start of the loop
                    continue
                if self.one_action_only:
                    self.option = mo_q.key
            # If option to execute, delete, edit or show one command is chosen
            if self.option in [mo_e.key, mo_d.key, mo_edit.key, mo_ss.key]:
                # Check if a command_id has been provided
                if self.command_id is None:
                    # If not, ask for one
                    self.command_id = InputWindow().ask_input(
                        msg='Command ID not found. Please enter ID: ',
                        valid_answers=self.valid_ids)
                    # If provided id is not and id but a request of an option
                    global_cmd = self.__global_option_checker(self.command_id)
                    if global_cmd:
                        continue
                # If command_id is provided
                if self.command_id is not None:
                    # If chosen option is to execute a command
                    if self.option == mo_e.key:
                        # Use option execute function and keep note whether error occurred
                        option_stopped = self.do_repeatable_menu_option(error=ValueError,
                                                                        menu_option=self.__option_to_execute)
                        # If error happened
                        if option_stopped:
                            # Go back to the start of the loop
                            continue
                        else:
                            print("----End of Terminal execute----")
                    # If chosen option is to delete a command
                    if self.option == mo_d.key:
                        # Use option delete function and keep note whether error occurred
                        option_stopped = self.do_repeatable_menu_option(error=ValueError,
                                                                        menu_option=self.__option_to_delete)
                        # If error happened
                        if option_stopped:
                            # Go back to the start of the loop
                            continue
                    # If chosen option is to edit the command
                    if self.option == mo_edit.key:
                        # Use option edit function and keep note whether error occurred
                        option_stopped = self.do_repeatable_menu_option(error=ValueError,
                                                                        menu_option=self.__option_to_edit)
                        # If error happened
                        if option_stopped:
                            # Go back to the start of the loop
                            continue
                    # If chosen option is to ss
                    if self.option == mo_ss.key:
                        # Use option to vire one command and keep note whether error occurred
                        option_stopped = self.do_repeatable_menu_option(error=ValueError,
                                                                        menu_option=self.__option_to_view_one_full_command)
                        # If error happened
                        if option_stopped:
                            # Go back to the start of the loop
                            continue
            # If option to add a command is chosen
            if self.option == mo_a.key:
                # Use option add function and keep note whether error occurred
                option_stopped = self.do_repeatable_menu_option(error=sqlite3.Error,
                                                                menu_option=self.__option_to_add)
                # If error happened
                if option_stopped:
                    # Go back to the start of the loop
                    continue
            # If option is 'exportall' do the disposition steps
            if self.option == mo_exp.key:
                # Export all
                SavedCommands().export_all()
                continue
            # If option is to repeat the last recorded action
            if self.option == mo_r.key:
                if self.last_command is not None:
                    # Assign the option last command
                    self.option = self.last_command
                    # Set command id to None so that user can
                    # pick the next command to manipulate
                    self.command_id = None
                    # Set repeat to True, so that the last used command is kept recorded.
                    self.repeat_last_command = True
                    # return to the start of the loop
                    continue
                # If something has gone wrong return to start
                else:
                    print('Sorry! It appears command to repeat was not found.')
                    continue
        # If the loop is broken, the user has chosen to leave the program.
        return 'CommandSaver program exited.'

    def convert_answer(self, answer):
        """
        Takes the answer and checks whether it is a command + option or just option.
        Returns: option and command_id
        """
        # Use regex to find the option string (any first letters)
        search1 = re.search(
            r'(^[a-z]+)', answer
        )
        # Check if a match was found
        if search1:
            # If so, make it the option
            option = search1.group(1)
        # If not,
        else:
            # Assign option as None
            option = None
            # and print an error
            StringFormatter(
                text_to_format='Error! Valid option has not been found.').print_red_bold()
            print('Please try again.')
            # and don't look any further
            return option, None
        if option == mo_t.key:
            search_text = re.search(
                r'([t])(.+)', answer
            )
            if search_text:
                command_id = search_text.group(2)
                print('text found= ', command_id)
                return option, command_id
            else:
                return option, None
        # Use regex to find the command integer (any first digit)
        search2 = re.search(
            r'([0-9]+)', answer
        )
        # Check if a match was found
        if search2:
            # and if so, assign it to the command_id
            command_id = search2.group(1)
            # if not text, make it an integer
            command_id = int(command_id)
            # then check if it is a valid integer
            # if it is valid
            if command_id in self.valid_ids:
                # pass and do nothing
                pass
            # but if not valid
            else:
                # return it as None
                command_id = None
        # if not,
        else:
            # make command_id None (stands for: no ID provided)
            command_id = None
        # return the option and command_id
        return option, command_id

    @staticmethod
    def __ask_command_description():
        """
        Asks user's input on the new command description.
        Returns: description provided by the user.

        """
        # ask table input for command_description
        msg_panel = '"Add new command" chosen, step 1 of 2. Please describe your command.\n' \
                    'The description will show up in the command menu. Try to be concise.'
        msg = 'The description: '
        # Ask user's input
        command_description = InputWindow().ask_input(msg=msg,
                                                      msg_info=msg_panel,
                                                      valid_answers='any_string',
                                                      )
        # Return the command description
        return command_description

    @staticmethod
    def __ask_new_command():
        """
        Asks user's input for the new terminal command.
        Returns: command provided by the user.

        """
        # Print a disclaimer/warning.
        StringFormatter('Caution! This program does no test the correctness of the command, make sure it works in the '
                        'terminal before submission.').print_red_bold()
        # ask table input for saved_command
        msg_panel = '\n"Add new command" chosen, step 2 of 2. \n' \
                    'Please write down the command that is to be executed.\n' \
                    'This is exactly what you would write in a terminal.'
        msg = "Terminal command: "
        # Ask user input
        new_command = InputWindow().ask_input(msg=msg,
                                              msg_info=msg_panel,
                                              valid_answers='any_string'
                                              )
        # Return the command
        return new_command

    def __global_option_checker(self, item_to_check):
        """
        Checks if the option is one of the global commands,
        if so updates the global option and repeat_last_command variable.
        Args:
            item_to_check: option to check

        Returns: True or False

        """
        # if an item is in the global command list
        if item_to_check in global_commands:
            # make option the request
            self.option = item_to_check
            # set the repeater to True to trigger the above option
            self.repeat_last_command = True
            # and return True
            return True
        # otherwise
        else:
            # return False
            return False

    def do_repeatable_menu_option(self, error, menu_option):
        """
        Calls menu option methods and updates the last command class field.
        Args:
            error: type of error that causes the method to be unusable.
            Could be a list of errors, e.g. [ValueError, OSError].
            menu_option: a method (function) that will be executed.

        Returns:

        """
        # Set last_used as current option
        self.last_command = self.option
        try:
            # Try to execute the function
            global_cmd = menu_option()
            # If user chooses to leave half way
            if global_cmd:
                # Return as True (option stopped)
                return True
        # If something went wrong an error was thrown
        # except if something went wrong or action was cancelled
        except error:
            # then return True(error occurred)
            return True

    def __option_to_execute(self):
        """
        Uses module to execute the command and
        to print out any instructions relevant to the command.

        """
        # Try to execute the command. OS sends the command to the terminal.
        SavedCommands(command_id=self.command_id).execute_command()
        # # Print success message if an error was not thrown
        # StringFormatter(text_to_format='Success! Command executed.').print_green_bold()

    def __option_to_execute_text_in_terminal(self):
        """
        Uses module to execute the command and
        to print out any instructions relevant to the command.

        """
        # Try to execute the command. OS sends the command to the terminal.
        SavedCommands(command_id=self.command_id, option=mo_t.key).execute_command(
            text_to_terminal=True, text_for_terminal=self.command_id)

    def __option_to_delete(self):
        """
        Uses external modules to delete the command and
        to print out any instructions relevant to the command.

        """
        # Delete the command
        SavedCommands(command_id=self.command_id).delete_command()

    def __option_to_edit(self):
        """
        Uses external modules to edit the command and
        to print out any instructions relevant to the command.

        """
        # Inform the user of the exit options
        ViewContents().print_input_window_table()
        # Launch the edit function
        edit_response = SavedCommands(
            command_id=self.command_id).edit_command()
        # Check if user chose to leave
        global_cmd = self.__global_option_checker(edit_response)
        # If so,
        if global_cmd:
            # go back to the start of the loop (return True to the caller)
            return True

    def __option_to_add(self):
        """
        Uses CommandSaver functions to add the command and
        to print out any instructions relevant to the command.

        """
        # Inform the user of the exit options
        ViewContents().print_input_window_table()
        # Ask description
        command_description = self.__ask_command_description()
        # Check if description is a global command
        global_cmd = self.__global_option_checker(command_description)
        # If so, return to the start of the loop
        if global_cmd:
            return True
        # Ask the new terminal command information
        new_command = self.__ask_new_command()
        # # Check if new command is a global command
        global_cmd = self.__global_option_checker(new_command)
        # If so, return to the start of the loop
        if global_cmd:
            return True
        # Launch add command function
        SavedCommands().add_new_command(command_description=command_description,
                                        new_command=new_command)

    def __option_to_setuserdep(self):
        """
        Uses CommandSaver functions to set author's department.

        """
        # Set last_used command as setuserdep
        self.last_command = mo_userdep.key
        # Call Change Author's Department function that handles department data
        department = UserData().change_authors_department()
        # # Check if new command is a global command
        global_cmd = self.__global_option_checker(department)
        # If so, return to the start of the loop
        if global_cmd:
            return True

    def __option_to_setuser(self):
        """
        Uses CommandSaver functions to set author's department.

        """
        # Set last_used command as setuser
        self.last_command = mo_username.key
        # Call Change Author function that handles author data
        username = UserData().change_author()
        # # Check if new command is a global command
        global_cmd = self.__global_option_checker(username)
        # If so, return to the start of the loop
        if global_cmd:
            return True

    def __option_to_view_one_full_command(self):
        """
        Uses CommandSaver functions to print one command with full details.

        """
        # Set last_used command as ss
        self.last_command = mo_ss.key
        # and print the command info
        ViewContents().print_one_full_command(command_id=self.command_id)
