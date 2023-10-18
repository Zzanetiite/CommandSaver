import logging
from command_saver.run_me import RunMe
from command_saver.constants import log_path


def main():
    # Set up logger configuration for the program.
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename=log_path,
                        filemode='w')
    # Run the program
    RunMe().run_program()


if __name__ == '__main__':
    main()
