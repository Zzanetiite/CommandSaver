from setuptools import setup, find_packages

setup(
    name="command-saver-terminal-program",
    version="2.0.3",
    description="Simple terminal helper program to save long terminal commands. See git: https://github.com/Zzanetiite/CommandSaver",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cs = command_saver.cs:main'
        ],
    },
)
