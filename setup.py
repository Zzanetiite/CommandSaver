from setuptools import setup, find_packages

setup(
    name="command-saver-terminal-program",
    version="2.0.2",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cs = command_saver.cs:main'
        ],
    },
)
