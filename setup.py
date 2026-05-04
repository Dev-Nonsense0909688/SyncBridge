from setuptools import setup, find_packages

setup(
    name="sync-bridge-core",
    version="0.1.0",
    description="SyncBridge core daemon + CLI",
    author="Dev-Nonsense0909688",
    license="MIT",
    packages=find_packages(),
    author_email="blackplasma001@gmail.com",
    platforms=["win32"],
    python_requires=">=3.8",
    package_dir={"": "."},
    entry_points={
        "console_scripts": [
            "sb=src.cli:main",
        ],
    },
)