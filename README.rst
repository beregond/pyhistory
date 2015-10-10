==============
Python History
==============

.. image:: https://badge.fury.io/py/pyhistory.png
    :target: http://badge.fury.io/py/pyhistory

.. image:: https://travis-ci.org/beregond/pyhistory.png?branch=master
        :target: https://travis-ci.org/beregond/pyhistory

.. image:: https://img.shields.io/pypi/dm/pyhistory.svg
        :target: https://pypi.python.org/pypi/pyhistory

.. image:: https://coveralls.io/repos/beregond/pyhistory/badge.png
    :target: https://coveralls.io/r/beregond/pyhistory


App to maintain history file for your project.

* Free software: BSD license
* Source: https://github.com/beregond/pyhistory
* PyPI: https://pypi.python.org/pypi/pyhistory

PyHistory
---------

PyHistory maintains history entries in distributed work environment, which
allows many developers to add/remove history entries between releases without
conflicts.

Installation
------------

.. code-block:: bash

  pip install pyhistory

Features
--------

(All commands can start either with `pyhistory` or shortcut - `pyhi`.)

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

    $ cat HISTORY.rst
    my project
    ==========

    0.4.1 (2015-08-04)
    ++++++++++++++++++

    * Added PyHistory to project.
    * Improved codebase.
    * Other features.

    $ pyhi update 0.4.2
    $ cat HISTORY.rst
    my project
    ==========

    0.4.2 (2015-08-05)
    ++++++++++++++++++

    * Bug fixes
    * Change in API
    * Removed old features

    0.4.1 (2015-08-04)
    ++++++++++++++++++

    * Added PyHistory to project
    * Improved codebase
    * Other features

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
    Do you really want to remove all entries? [y/N]: y

  Or without prompt:

  .. code-block:: bash

    $ pyhi clear --yes

Config file
-----------

You can adjust Pyhistory behaviour to your needs by ``setup.cfg`` file. Just
put ``pyhistory`` section in there:

.. code-block:: ini

  [pyhistory]
  history_dir = some_dir  # 'history' by default
  history_file = myhistory.rst  # 'HISTORY.rst' by default
  at_line = 42  # by default history will be injected after first headline
