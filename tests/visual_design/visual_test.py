# This file is used to test visual output only.
# Test is manual, developer may test the output
# by looking at it in the terminal.
from command_saver.visual_design.formatter import StringFormatter, TableFormatter, PanelFormatter
from command_saver.utils.default_database import DefaultDatabase

from command_saver.visual_design.view_contents import ViewContents

# Set up string to test.
string_to_test = 'String test!\nThis could be multiple lines.'
# Set up a header to test
simple_panel = ['Title', 'Header information.']
panel_w_paragraphs = ['Title', 'Header information.',
                      'some info', 'some more info']

# Set up table data to test.
test = DefaultDatabase()
list_of_data = test.saved_commands_data
table_title = 'Saved Commands'
list_of_menu_data = test.menu_options_data
table_menu_title = 'Menu Options'

# Expecting green bold output.
StringFormatter(text_to_format=string_to_test).print_green_bold()
# Pass, date 30/03/2023

# Expecting red bold output.
StringFormatter(text_to_format=string_to_test).print_red_bold()
# Pass, date 30/03/2023

# Expecting a table of saved commands as output.
TableFormatter(table_title=table_title,
               list_to_format=list_of_data).print_table_saved_commands()
# Pass, date 30/03/2023


# Expecting a panel with title as output.
PanelFormatter(panel_to_format=simple_panel).print_panel()
# Pass, date 30/03/2023

# Expecting a panel without title as output.
PanelFormatter(panel_to_format=[string_to_test]).print_panel()
# Pass, date 30/03/2023

# Expecting a panel with title and paragraphs.
PanelFormatter(panel_to_format=panel_w_paragraphs).print_panel()
# Pass, date 30/03/2023

# Expecting a table of menu options as output.
# Expecting an empty row between some commands.
TableFormatter(table_title=table_menu_title,
               list_to_format=list_of_menu_data).print_table_menu_options()
# Pass, date 30/03/2023


# MOVED from test_view_contents, which has been deleted.
# Visual output testing
# Test Main Menu layout
ViewContents().print_main_menu()
# Test Saved Commands Menu layout
ViewContents().print_saved_commands_menu()
# Test input window table content
ViewContents().print_input_window_table()
# Test help page layout
ViewContents().print_help_page()
# Test one option - make sure 1 exists or this will fail!
ViewContents().print_one_full_command(command_id=1)
