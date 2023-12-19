import subprocess

from setuptools import setup, find_packages
from setuptools.command.install import install

setup(
    name='YoLinkPy',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Add your package dependencies here
        'numpy',
        'yolink-api',
        'requests',
        'python-dotenv',
        # ...
    ]
)
