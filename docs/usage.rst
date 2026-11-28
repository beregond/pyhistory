=====
Usage
=====

PyHistory is a command line tool. Every command can be run either as
``pyhistory`` or with the shortcut ``pyhi``.

Typical workflow
----------------

1. With every change, add a history entry instead of editing the history file
   directly::

       $ pyhi add "Added support for python 3.15."

   Each entry is stored as a separate file in the ``history`` directory, so
   entries added on different branches never conflict. Commit that file
   together with your change.

2. Check what will land in the next release::

       $ pyhi list

3. On release, move all pending entries into the history file under the new
   version::

       $ pyhi update 1.2.0

Commands
--------

``add MESSAGE``
    Add a new history entry.

``list``
    Show pending entries.

``update VERSION``
    Insert pending entries into the history file as a new release section and
    remove them from the history directory. Options: ``--date``,
    ``--at-line``, ``--line-length`` (rst only), ``--md-header-level``
    (markdown only).

``delete [ENTRY]...``
    Without arguments, list numbered entries. With numbers, delete the chosen
    entries.

``clear``
    Remove all pending entries (``--yes`` skips the confirmation prompt).

Run ``pyhi COMMAND --help`` for all options of a command.

Configuration
-------------

Locations of the history directory and history file, and other settings, can
be set in ``pyproject.toml`` (``[tool.pyhistory]``) or ``setup.cfg``
(``[pyhistory]``). See the *Config file* section of :doc:`readme` for details.
