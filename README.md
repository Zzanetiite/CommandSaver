# CommandSaver
CommandSaver is a console-interface application that saves and executes terminal commands added by the user.

### Summary
The purpose of the program is to help the user keep track of commonly used complicated commands. It is a lot like aliases.

## Installation via Pip
Use this command to install the package.
```
pip install command-saver-terminal-program
```

Or

```
pip install --user command-saver-terminal-program
```

## Running in the terminal
Use `cs` to launch the program in the terminal.
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
pip install --user dist/command-saver-terminal-program-2.1.3.tar.gz
```


