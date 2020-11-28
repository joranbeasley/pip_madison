=====
Usage
=====

Generally pip-madison is expected to be used as a command line tool

.. code-block:: bash

   user@home:~ $ pip-madison --help
   Usage: pip-madison [OPTIONS] PACKAGE_NAME
     PACAKAGE_NAME is the name of the package to inspect, you can optionally
     include specific pypi indexes to search

     eg. `$ pip-madison numpy https://user:passwd@my.pypi.org/simple`

   Options:
     -r, --repository TEXT           optionally supply one or more repositories
                                     to search (can be used multiple times)

     -q, --quiet                     only print the version numbers (equivelent
                                     to --format "{ver}")

     --latest                        if set only print the latest version
     -t, --type [.tar.gz|.zip|.whl|.exe]
                                     the fileType to search for.
                                     see also `pip-madison help types`

     --py PY_CODE                    the pip format python version to check. see
                                     `pip-madison help python`

     -a, --os OS_CODE                the operating system to check against.
                                     see also `pip-madison help os`

     -f, --format TEXT               the format to use:
                                     see `pip-madison help format`

     --help                          Show this message and exit.

we are more interested in the API in this documentation
