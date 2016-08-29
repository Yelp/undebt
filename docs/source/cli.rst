Undebt_: Command Line Interface
===============================

.. _Undebt: index.html
.. default-role:: code

Install it
----------

.. code-block:: bash

    $ git clone https://github.com/Yelp/undebt.git
    $ cd undebt
    $ pip install .

Read it
-------

.. code-block:: bash

    $ undebt --help
    usage: undebt [-h] --pattern path [--extension ext]
                  [--multiprocess processes] [--verbose] [--dry-run]
                  [PATH [PATH...]]

    positional arguments:
      PATH [PATH...]
                            paths to files or directories (searched recursively
                            for extension) to be modified (if not passed uses
                            stdin)

    optional arguments:
      -h, --help            show this help message and exit
      --pattern path, -p path
                            paths to pattern definition files
      --extension ext, -e ext
                            extensions of files to be modified when searching a
                            directory (exclude ".", e.g. "py" instead of ".py")
      --multiprocess processes, -m processes
                            number of processes to run in parallel (default is 16)
      --verbose
      --dry-run, -d         only print to stdout; do not overwrite files

Try it out
----------

.. code-block:: bash

    $ undebt -p ./undebt/examples/method_to_function.py ./tests/inputs/method_to_function_input.txt
    $ git diff
    diff --git a/tests/inputs/method_to_function_input.txt b/tests/inputs/method_to_function_input.txt
    index f268ab9..7681c63 100644
    --- a/tests/inputs/method_to_function_input.txt
    +++ b/tests/inputs/method_to_function_input.txt
    @@ -1,13 +1,14 @@
    +from function_lives_here import function
     something before code pattern
     @decorator([Class])
     def some_function(self, abc, xyz):
         """herp the derp while also derping and herping"""
         cde = fgh(self.l)
         ijk = cde.herp(
    -        opq_foo=FOO(abc).method()
    +        opq_foo=function(FOO(abc))
         )['str']
         lmn = cde.herp(
    -        opq_foo=FOO(xyz).method()
    +        opq_foo=function(FOO(xyz))
         )['str']
     bla bla bla
         for str_data in derp_data['data']['strs']:
    @@ -16,8 +17,8 @@ bla bla bla
                 rst.uvw(
                     CTA_BUSINESS_PLATFORM_DISABLED_LOG,
                     "derp {derp_foo} herp {herp_foo}".format(
    -                    derp_foo=FOO(derp_foo).method(),
    -                    herp_foo=FOO(herp_foo).method(),
    +                    derp_foo=function(FOO(derp_foo)),
    +                    herp_foo=function(FOO(herp_foo)),
                     ),
                 )
     something after code pattern

Tips and Tricks
---------------

Most of these will make use of
```xargs`` <http://man7.org/linux/man-pages/man1/xargs.1.html>`_

Using with ``grep``/``git grep`` to find files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    grep -l <search-text> **/*.css | xargs undebt -p <path-to-pattern>
    # Use git grep if you only want to search tracked files
    git grep -l <search-text> | xargs undebt -p <path-to-pattern>

Using ``find`` to limit to a particular extension
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    find -name '*.js' | xargs grep -l <search-text> | xargs undebt -p <path-to-pattern>

Using ``xargs`` to work in parallel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``xargs`` takes a ``-P`` flag, which specifies the maximum number of processes
to use.

.. code-block:: bash

    git grep -l <search-text> | xargs -P <numprocs> undebt -p <path-to-pattern>
