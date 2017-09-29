#!/usr/bin/env python
# coding: utf-8

import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

from pyhistory import __version__, __author__, __email__, __description__


PROJECT_NAME = 'pyhistory'


class PyTest(TestCommand):

    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['--cov', PROJECT_NAME]

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


setup(
    name=PROJECT_NAME,
    version=__version__,
    description=__description__,
    long_description=readme + '\n\n' + history,
    author=__author__,
    author_email=__email__,
    url='https://github.com/beregond/pyhistory',
    packages=[
        PROJECT_NAME,
    ],
    package_dir={
        PROJECT_NAME: PROJECT_NAME,
    },
    include_package_data=True,
    install_requires=[
        'click',
        'pathlib',
        'six',
    ],
    entry_points={
        'console_scripts': [
            'pyhistory = pyhistory.cli:main',
            'pyhi = pyhistory.cli:main',
        ]
    },
    license="BSD",
    zip_safe=False,
    keywords='pyhistory',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    cmdclass={
        'test': PyTest,
    },
)
