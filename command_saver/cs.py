import logging
from command_saver.run_me import RunMe
from constants import log_path

# Set up logger configuration for the program.
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=log_path,
                    filemode='w')
# Run the program
print(RunMe().run_program())
