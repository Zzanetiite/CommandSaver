from rich import print as rprint
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from typing import List
from command_saver.constants import items_before_break


class StringFormatter:
    """Class that takes text and formats it according to design."""

    def __init__(
            self,
            text_to_format: str
    ):
        """
        Application's text formatter. Takes text and formats it according to design.
        Args:
            text_to_format: text string to format.
        """
        self.text_to_format = text_to_format

    def print_green_bold(self):
        """
        Prints the text given to the class in bold green.

        """
        rprint(f"[bold green]{self.text_to_format}[/bold green]")

    def print_red_bold(self):
        """
        Prints the text given to the class in bold green.

        """
        rprint(f"[bold red]{self.text_to_format}[/bold red]")


class TableFormatter:
    """Class that takes text and formats it according to design."""

    def __init__(
            self,
            list_to_format: List[str],
            table_title: str = None,
    ):
        """
        Application's table formatter. Takes a list and formats it according to design.
        Args:
            list_to_format: table data to format.
            table_title: table title.
        """
        self.list_to_format = list_to_format
        self.table_title = table_title

    def print_table_saved_commands(self):
        """
        Prints saved commands table with the given table title and list of items.

        """
        # Set table header
        table = Table(title=self.table_title)
        # Create table headers for columns to print
        headers = ['Command ID', 'Description', 'Terminal Command']
        # for each header in the list
        for header in headers:
            # add a column to the table
            table.add_column(header, justify="left")
        # If no entries, don't do anything, return an empty table to the user
        if len(self.list_to_format) == 0:
            pass
        else:
            # If list has 3 items it is recent commands list: it is already sorted
            if len(self.list_to_format[0]) != 3:
                # Sort data by most used. Tuple[5] is the "times called" item in the list.
                self.list_to_format.sort(key=lambda tup: tup[5], reverse=True)
            # Create rows and fill them with data of first three items in each tuple.
            # For an item in the given list
            for item in self.list_to_format:
                # add a row with each command's ID, description and terminal command
                table.add_row(str(item[0]), str(item[1]), str(item[2]))
        # Console needed for rich module to print panels
        console = Console()
        # Print the table
        console.print(table)

    def print_table_menu_options(self):
        """
        Prints Menu Options table with a given heading and given list of options.

        """
        # Set table header
        table = Table(title=self.table_title)
        # Create table headers for columns to print
        headers = ['Option', 'Description']
        # for header in the list
        for header in headers:
            # add a column
            table.add_column(header, justify="left")
        # Create rows and fill them with data, separate them with a break as per program design document.
        # Separate menu options that go before and after the break.
        items_after_break = []
        # for an item in the menu options list
        for item in self.list_to_format:
            # check if it is the before-break option
            if item[1] in items_before_break:
                # and if it is, add it as a row in the table
                table.add_row(str(item[1]), str(item[2]))
            # if it is not pre-break item,
            else:
                # add it to the after-break list
                items_after_break.append(item)
        # Add the empty row (as per design)
        table.add_row()
        # for an item in the after-break option's list
        for item in items_after_break:
            # add a row in the table
            table.add_row(str(item[1]), str(item[2]))
        # Console needed for rich module to print panels
        console = Console()
        # Print the table
        console.print(table)

    def print_table_one_command(self, command_id: str):
        """
        Prints saved commands table with one given command.

        """
        # Set table header
        table = Table()
        # Create table headers for columns to print
        headers = ['Command ID', 'Unique Database ID', 'Description', 'Terminal Command',
                   'Date Created', 'First-Made Timestamp', 'Times executed',
                   'Author', 'Last-Edited Timestamp']
        # for each header in the list
        for header in headers:
            # add a column to the table
            table.add_column(header, justify="left")
        # Create rows and fill them with data of the tuple.
        # For an item in the given list
        for item in self.list_to_format:
            # add a row with each command's ID, description and terminal command
            table.add_row(str(command_id), str(item[0]), str(item[1]), str(item[2]),
                          str(item[3]), str(item[4]), str(item[5]),
                          str(item[6]), str(item[7]))
        # Console needed for rich module to print panels
        console = Console()
        # Print the table
        console.print(table)


class PanelFormatter:
    """Class that takes text and formats it according to design."""

    def __init__(self, panel_to_format: List[str]):
        """
        Application's text formatter. Takes text and formats it according to design.
        Args:
            panel_to_format: header string to format.
        """
        self.panel_to_format = panel_to_format

    def print_panel(self):
        """
        Prints a panel of data from a list of given data. If only single item in the list is given,
        that is printed as  text in the panel and panel has no heading.
        If more, first item in the list is a panel heading and the rest are text in the panel.
        Each item in the list is printed in a new line.

        """
        # if there is only one string, panel has no title
        if len(self.panel_to_format) == 1:
            # Print a panel with a single line of text within
            rprint(Panel(self.panel_to_format[0]))
        # if there is are two strings, panel has a title
        elif len(self.panel_to_format) == 2:
            # take entry 0 of the list as heading and the other entry as text
            rprint(Panel(self.panel_to_format[1],
                   title=self.panel_to_format[0]))
        # if there are more than two strings, there is more than one paragraph
        else:
            # join paragraphs in a string with line break in-between them, except first entry
            text_string = '\n'.join(
                self.panel_to_format[1:(len(self.panel_to_format))])
            # first entry is a heading. Print the panel.
            rprint(Panel(text_string, title=self.panel_to_format[0]))
