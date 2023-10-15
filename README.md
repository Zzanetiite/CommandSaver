# CommandSaver
CommandSaver is a console-interface application that saves and executes terminal commands added by the user.

### Summary
The purpose of the program is to help the user keep track of commonly used complicated commands. It is a lot like aliases.

### Development pre-requisites
Please see requirements.txt for any necessary packages.

### Explanation of development
Project is developed using PyCharm integrated development environment (IDE) and in accordance with the design of Software Engineering Fundamentals final assignment. 

#### How do I run this on my machine?
1. Ensure requirements are installed.
2. Use Pycharm or similar Python interpreter.
3. Setup a path in bash or zsh to run it from terminal.

## Documentation
For any additional details on the design and project see Software Engineering Fundamentals final assignment.

Read more about rich package here: https://rich.readthedocs.io/en/stable/tables.html

Read more about logger here: https://docs.python.org/3/library/logging.html

Read more about mock objects used for unit tests here: https://docs.python.org/3/library/unittest.mock.html?highlight=patch#module-unittest.mock

## Development
This program has no dependencies, other than ones described in the requirements.txt file.

This program has a comment for almost every line of the code, this was a requirement for the coursework assignment.

### Testing
To test unittests, call them in the terminal using python or use Python interpreter. Tests have not been updated for CommandSaver version 2.0 (outdated from 1.0 - didn't have the time to do them).

### Running
To run the program use Python to open the cs.py file in the command_saver folder or call from the terminal.

### Deploying
Run the program through terminal using `cs OPTION COMMAND_ID` or via python calling the `cs.py`.

### Packaging
To package program with changes use:
```
pip install setuptools wheel
python setup.py sdist bdist_wheel
```

To distribute package use in IDE:
```
pip install twine
```

And afterwards, in the command prompt:
```
twine upload dist/*
```

## Installation via Pip
Use this command to install the package.
```
pip install command-saver-terminal-program
```

Use `cs` to launch the program in the terminal.
