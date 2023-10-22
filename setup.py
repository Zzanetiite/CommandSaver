from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name="command-saver-terminal-program",
    version="2.1.3",
    description="Simple terminal helper program to save long terminal commands. See git: https://github.com/Zzanetiite/CommandSaver",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cs = command_saver.cs:main'
        ],
    },
    install_requires=[
        'rich==13.3.3',
    ],
)
