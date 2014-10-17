.. :changelog:

History
-------

1.3 (2014-10-17)
++++++++++++++++

* Timestamps are now in miliseconds (again).
* Added load config from file.

1.2.1 (2014-08-06)
++++++++++++++++++

* Improved format of generated hash (no miliseconds now).

1.2 (2014-07-22)
++++++++++++++++

* Added delete command.

1.1 (2014-07-15)
++++++++++++++++

* Added timestamp to generated files, so now entries are properly ordered.
* Pyhistory traverses directory tree to find proper place for history directory.

1.0.3 (2014-06-23)
++++++++++++++++++

* Added squash command (alias to update).

1.0.2 (2014-06-22)
++++++++++++++++++

* Further bug fixing of start detecting.

1.0.1 (2014-06-20)
++++++++++++++++++

* Fixed error raised by `clear` when history dir is absent.
* Fixed `update` - command will now try to find file start.

1.0 (2014-06-20)
++++++++++++++++

* First release on PyPI.
