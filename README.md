# PyHistory

[![PyPI version](https://badge.fury.io/py/pyhistory.svg?icon=si%3Apython)](https://badge.fury.io/py/pyhistory)
[![PyPI Downloads](https://static.pepy.tech/badge/pyhistory)](https://pepy.tech/projects/pyhistory)

App to maintain history file for your project.

* Free software: BSD license
* Source: <https://github.com/beregond/pyhistory>
* PyPI: <https://pypi.python.org/pypi/pyhistory>
* ReadTheDocs: <https://pyhistory.readthedocs.io/en/latest/>

PyHistory maintains history entries in distributed work environment, which
allows many developers to add/remove history entries between releases without
conflicts.

## Installation

```bash
pip install pyhistory
```

## Features

(All commands can start either with `pyhistory` or shortcut - `pyhi`.)

* Add history entry:

  ```bash
  pyhi add 'New feature'
  pyhi add Something
  ```

* List history entries:

  ```bash
  $ pyhi list

  * New feature
  * Something
  ```

* Update your history file with entries for given release:

  ```bash
  $ cat HISTORY.rst
  my project
  ==========

  0.4.1 (2015-08-04)
  ++++++++++++++++++

  * Added PyHistory to project.
  * Improved codebase.
  * Other features.
  ```

  ```bash
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
  ```

* Delete selected entries:

  ```bash
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
  ```

* Clear all history:

  ```bash
  $ pyhi clear
  Do you really want to remove all entries? [y/N]: y
  ```

  Or without prompt:

  ```bash
  pyhi clear --yes
  ```

## Config file

(``setup.cfg`` has precedence over ``pyproject.toml`` for backward compatibility!)

You can adjust Pyhistory behaviour to your needs by adding config to ``pyproject.toml`` file:

```toml
  [tool.pyhistory]
  history_dir = "some_dir"  # 'history' by default
  history_file = "myhistory.md"  # 'HISTORY.rst' by default
  at_line = 42  # by default history will be injected after first headline
```

You can also add config to ``setup.cfg`` file. Just put ``pyhistory`` section in there:

```ini
  [pyhistory]
  history_dir = some_dir
  history_file = myhistory.rst
  at_line = 42
```

## Differences in formatting

If you are using markdown format you must note that:

* Lines are not wrapped, setting for line length is ignored
* There is extra config for markdown formatting - `md_header_level` (default is 2) and it sets amount of `#` in headline for version
