===============================
Python History
===============================

.. image:: https://badge.fury.io/py/pyhistory.png
    :target: http://badge.fury.io/py/pyhistory

.. image:: https://travis-ci.org/beregond/pyhistory.png?branch=master
        :target: https://travis-ci.org/beregond/pyhistory

.. image:: https://pypip.in/d/pyhistory/badge.png
        :target: https://pypi.python.org/pypi/pyhistory


Package to help maintaining HISTORY file for Python project.

* Free software: BSD license
* Documentation: http://pyhistory.readthedocs.org.

Note
----

This package is created to help maintaining history file in environment of high
concurrency (literally: each pull request on GitHub had conflicts in
HISTORY.rst file because it was updated before creating PR). Take into account
it may NOT fit into your environment and/or workflow since it was cutted for
specific case, but it's good if so. :)

Features
--------

(All commands can start either with `pyhistory` or `pyhi`.)

* Add history entry:

.. code-block:: bash

    $ pyhi add 'New feature'
    $ pyhi add Something

* List history entries:

.. code-block:: bash

    $ pyhi list

    * New feature
    * Something

* Update your history file with entries for given release:

.. code-block:: bash

    $ pyhi update 0.4.2

* Clear history:

.. code-block:: bash

    $ pyhi clear
