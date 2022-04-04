from setuptools import setup

from pyhistory import __author__, __description__, __email__, __version__

PROJECT_NAME = "pyhistory"

readme = open("README.rst").read()
history = open("HISTORY.rst").read().replace(".. :changelog:", "")


setup(
    name=PROJECT_NAME,
    version=__version__,
    description=__description__,
    long_description=readme + "\n\n" + history,
    author=__author__,
    author_email=__email__,
    url="https://github.com/beregond/pyhistory",
    packages=[
        PROJECT_NAME,
    ],
    package_dir={
        PROJECT_NAME: PROJECT_NAME,
    },
    include_package_data=True,
    install_requires=[
        "click",
    ],
    entry_points={
        "console_scripts": [
            "pyhistory = pyhistory.cli:main",
            "pyhi = pyhistory.cli:main",
        ]
    },
    license="BSD",
    zip_safe=False,
    keywords="pyhistory",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
