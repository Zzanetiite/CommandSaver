from typing import List
from command_saver.visual_design.formatter import StringFormatter, PanelFormatter, TableFormatter
from command_saver.table.saved_commands import SavedCommands
from command_saver.table.menu_options import MenuOptions
from command_saver.constants import (
    help_menu_info,
    main_menu_info,
    saved_commands_info,
    options_within_main_menu,
    options_within_input_menu
)


class ViewContents:
    """
    Consists of components that are printed to form layout views.
    """

    def __init__(self):
        """
        Parameters used for the prints.
        """
        # Page contents
        self.help_menu_info = help_menu_info
        self.main_menu_info = main_menu_info
        self.saved_commands_info = saved_commands_info

        # Fetch table data that is to be displayed in the layouts
        self.recent_commands_list = SavedCommands().recent_commands_list()
        self.all_saved_commands_list = SavedCommands().view_all_saved_commands()
        self.menu_options_list = MenuOptions().view_options()

    @staticmethod
    def print_success_msg(msg, information):
        """
        Prints the success message in green bold.
        Args:
            msg: message to print in green bold.
            information: any additional information to print under the message (basic format).

        Returns: prints formatted information in the terminal.

        """
        StringFormatter(text_to_format=msg).print_green_bold()
        print(information)

    @staticmethod
    def print_failure_msg(msg, information):
        """
        Prints the success message in red bold.
        Args:
            msg: message to print in red bold.
            information: any additional information to print under the message (basic format).

        Returns: prints formatted information in the terminal.

        """
        StringFormatter(text_to_format=msg).print_green_bold()
        print(information)

    def __available_options(self, available_list: List[str]):
        """
        Takes Menu Options and removes options that are not available.
        Args:
            available_list: list of menu options available at this stage.

        Returns: a list of available menu options.

        """
        # prepare a placeholder list
        return_list = []
        # use all menu options list
        t = self.menu_options_list
        # for an item in the menu options list
        for i in range(len(t)):
            # if item is in the current menu list
            if t[i][1] in available_list:
                # add it to the placeholder list
                return_list.append((t[i]))
        # return a list with only available options
        return return_list

    def __find_option(self, opt):
        """
        Takes an option and searches for it in the options menu  list.
        Args:
            opt: option to search for.

        Returns: option letter and description.

        """
        # create a placeholder for the description
        description = None
        # use all menu options list
        t = self.menu_options_list
        # for an item in the menu options list
        for i in range(len(t)):
            # if the item is the same option as desired option (this value is unique in the table)
            if t[i][1] == opt:
                # fetch the item's description
                description = t[i][2]
                # and stop searching
                break
        # return the option's description
        return description

    def print_main_menu(self):
        """
        Prints a formatted Main Menu of the application.
        Returns: prints the menu in the terminal.

        """
        # Print the header part of the main menu
        PanelFormatter(panel_to_format=self.main_menu_info).print_panel()
        # Prepare options available in the main menu
        available_options = self.__available_options(
            available_list=options_within_main_menu)
        # Print the Menu Options table that shows options available in the Main Menu
        TableFormatter(list_to_format=available_options,
                       table_title='MENU OPTIONS').print_table_menu_options()
        # Print the Recent Commands table using saved commands printing arrangement
        TableFormatter(list_to_format=self.recent_commands_list,
                       table_title='SAVED COMMANDS SUMMARY').print_table_saved_commands()

    def print_saved_commands_menu(self):
        """
        Prints a formatted Saved Commands menu of the application.
        Returns: prints the commands in the terminal.

        """
        # Print the Saved Commands table with all saved commands options
        TableFormatter(list_to_format=self.all_saved_commands_list,
                       table_title='SAVED COMMANDS').print_table_saved_commands()

    def print_input_window_table(self):
        """
        Prints the table that shows available menu options before the input window.
        Returns: prints a table of available options.

        """
        # Prepare options available at this point
        available_options = self.__available_options(
            available_list=options_within_input_menu)
        # Print the Menu Options table that shows options available at this point
        TableFormatter(list_to_format=available_options,
                       table_title='OPTIONS AVAILABLE AT ANY POINT').print_table_menu_options()

    def print_help_page(self):
        """
        Prints the help page.
        Returns: help page printed in the terminal.

        """
        # Print the header part of the help menu panel
        PanelFormatter(panel_to_format=self.help_menu_info).print_panel()
        # Print the Menu Options table that shows options available at this point
        TableFormatter(list_to_format=self.menu_options_list,
                       table_title='ALL MENU OPTIONS AVAILABLE AT DIFFERENT STAGES').print_table_menu_options()

    @staticmethod
    def print_one_full_command(command_id):
        """
        Prints one full command.

        """
        # fetch the command
        one_full_command = SavedCommands(
            command_id=command_id).fetch_one_full_command()
        # Print a table that shows command data
        TableFormatter(list_to_format=one_full_command).print_table_one_command(
            command_id=command_id)
