==============
Python History
==============

.. image:: https://badge.fury.io/py/pyhistory.png
    :target: http://badge.fury.io/py/pyhistory

.. image:: https://travis-ci.org/beregond/pyhistory.png?branch=master
        :target: https://travis-ci.org/beregond/pyhistory

.. image:: https://img.shields.io/pypi/dm/pyhistory.svg
        :target: https://pypi.python.org/pypi/pyhistory


Package to help maintaining HISTORY file for Python project.

* Free software: BSD license
* Source: https://github.com/beregond/pyhistory

Note
----

This package is created to help maintaining history file in environment of high
concurrency (literally: each pull request on GitHub had conflicts in
HISTORY.rst file because it was updated before creating PR). Take into account
it may NOT fit into your environment and/or workflow since it was cutted for
specific case, but it's good if so. :)

History directory
-----------------

Pyhistory will traverse directory tree until it finds ``history file`` (by
default ``HISTORY.rst``, can be changed in ``setup.cfg``, see section ``Config
file``) and this will be root, where history directory will be created, in
which all entries will be stored. Thanks to that you can add, list or remove
entries from any point in your project - all commands will be executed in
context of root directory.

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

* Delete selected entries:

  .. code-block:: bash

    $ pyhi delete

    1. New feature
    2. Something
    3. Another one
    4. Wrong one

    (Delete by choosing entries numbers.)

    $ pyhi delete 2 4
    $ pyhi list

    * New feature
    * Another one

* Clear all history:

  .. code-block:: bash

    $ pyhi clear

* Config file:

  You can adjust Pyhistory behaviour to your needs by ``setup.cfg`` file. Just
  put ``pyhistory`` section in there:

  .. code-block:: ini

    [pyhistory]
    history_dir = some_dir # 'history' by default
    history_file = myhistory.rst # 'HISTORY.rst' by default
    at_line = 42 # By default history will be injected after first header
