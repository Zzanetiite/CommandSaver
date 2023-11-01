# CommandSaver
CommandSaver is a console-interface application that saves and executes terminal commands added by the user.

### Summary
The purpose of the program is to help the user keep track of commonly used complicated commands. It is a lot like aliases.

## Installation
Install the package in the user directory using:

```
pip install --user command-saver-terminal-program
```

Close the shell, start a new shell and use `cs` to run.

### If command not found error happens

This error happens when the script path hasn't been added to the user's directory. Check whether the installation directory is included in the user's PATH. If not, modify your shell configuration file (e.g., ~/.bashrc or ~/.zshrc) to include it. For example, you can add the following line to your ~/.zshrc file:

```
export PATH=/local/home/username/.local/bin:$PATH
```

## Running in the terminal
Use `cs` to launch the program from bash or zsh.
Or run a single command using `cs OPTION COMMAND_ID`

# Development

Project has been developed using PyCharm integrated development environment (IDE) and in accordance with the design of Software Engineering Fundamentals final assignment (University assignment). 

## Documentation
Read more about rich package here: https://rich.readthedocs.io/en/stable/tables.html

Read more about logger here: https://docs.python.org/3/library/logging.html

Read more about mock objects used for unit tests here: https://docs.python.org/3/library/unittest.mock.html?highlight=patch#module-unittest.mock

Additional details on the design and the project have been described in the Software Engineering Fundamentals final assignment.

## Development

The code has a comment in almost every line, this was the coursework requirement.

### Testing
Unit tests have been called them in the terminal using python. Tests have not been updated for CommandSaver versions >2.0 (outdated from 1.0 - didn't have time to do them).

### Packaging & Deployment
Packaged using:
```
pip install setuptools wheel
```

```
python setup.py sdist bdist_wheel
```

Distributed via PyPI using twine:
```
pip install twine
```

```
twine upload dist/*
```

Locally tested using:
```
pip install --user dist/command-saver-terminal-program-2.2.2.tar.gz
```


