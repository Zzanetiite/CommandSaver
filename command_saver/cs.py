import logging
from command_saver.run_me import RunMe
from constants import log_path

def main():
    # Set up logger configuration for the program.
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename=log_path,
                        filemode='w')
    # Run the program
    result = RunMe().run_program()
    print(result)

if __name__ == '__main__':
    main()
