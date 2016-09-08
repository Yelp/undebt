Undebt_: Contributing
==========================

.. _Undebt: index.html
.. default-role:: code

Getting Started
---------------

Undebt's development is taking place on Github, so please go ahead and `fork`_ the repository if you want to begin contributing.

.. _`fork`: https://github.com/Yelp/undebt#fork-destination-box

You'll then want to get a local copy of the code base:

.. code-block:: bash

    git clone git@github.com:<your-username>/undebt.git

Getting Setup
-------------

It is highly recommended that you create a `virtual environment`_ before installing the project dependencies.

.. _`virtual environment`: http://docs.python-guide.org/en/latest/dev/virtualenvs/

You can achieve both (create a virtualenv and install dependencies) with:

.. code-block:: bash

    make dev

Running the Tests
-----------------

Undebt uses `tox`_ for testing.

.. _`tox`: https://tox.readthedocs.io/en/latest/

You can run the entire test suite:

.. code-block:: bash

    make test

Or, run an individual environment:

.. code-block:: bash

    tox -e py35  # probably need to be virtualenv

Note. If you do not have the required dependencies for each Tox environment, you will receive an error.
Avoid this by passing the `--skip-missing-interpreters` option.

Adding Documentation
--------------------

Undebt's documentation is formatted using  `reStructuredText`_ and hosted on `RTD`_.
Please try to follow the existing style and organization patterns.

.. _`reStructuredText`: http://docutils.sourceforge.net/rst.html
.. _`RTD`: http://undebt.readthedocs.io/en/latest/

You can test your contribution with:

.. code-block:: bash

    make docs

Your new, local documentation will be available at `docs/build/html/`.
