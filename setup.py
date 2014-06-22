#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = []

setup(
    name='pyhistory',
    version='1.0.2',
    description='Package to help maintaining HISTORY file for Python project.',
    long_description=readme + '\n\n' + history,
    author='Szczepan Cieślik',
    author_email='szczepan.cieslik@gmail.com',
    url='https://github.com/beregond/pyhistory',
    packages=[
        'pyhistory',
    ],
    package_dir={
        'pyhistory': 'pyhistory',
    },
    include_package_data=True,
    install_requires=requirements,
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
    ],
    test_suite='tests',
)
