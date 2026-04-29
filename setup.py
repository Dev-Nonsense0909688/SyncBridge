from setuptools import setup, find_packages

setup(
    name="sync-bridge",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "sb=src.cli:main", 
        ],
    },
)