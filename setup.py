#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from shutil import rmtree

from setuptools import setup, Command

# Package meta-data.
NAME = 'nrql-simple'
DESCRIPTION = 'A dead-simple tool to interact with the New Relic Insights query API. You can interact with this library programmatically or via the Command Line.'
URL = 'https://github.com/anthonybloomer/nrql-simple'
EMAIL = 'ant0@protonmail.ch'
AUTHOR = 'Anthony Bloomer'
REQUIRES_PYTHON = '>=2.7.10'
VERSION = "1.0.1"
LICENSE = 'MIT'
REQUIRED = [
    'requests', 'pygments'
]

here = os.path.abspath(os.path.dirname(__file__))

with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")

class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git push --tags')

        sys.exit()


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_descr=long_descr,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    py_modules=['nrql'],
    entry_points={
        'console_scripts': ['nrql=app:main'],
    },
    install_requires=REQUIRED,
    include_package_data=True,
    license=LICENSE,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        "Topic :: Software Development :: Libraries",
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    cmdclass={
        'upload': UploadCommand,
    },
)
