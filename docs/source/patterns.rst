Undebt_: Pattern Files
======================

.. _Undebt: index.html
.. default-role:: code

Undebt requires a pattern file that describes what to replace and how to replace it. There are two different ways to write pattern files: old/basic style, and new/advanced style. Unless you know you need multi-pass parsing, you should use old/basic style by default.

Old/Basic Style
---------------

When writing an old/basic style pattern, you must define the following names in your pattern file:

- `grammar` defines what pattern you want to replace, and must be a pyparsing_ grammar object.
- `replace` is a function that takes one argument, the tokens produced by `grammar`, and returns the string they should be replaced with, or `None` to do nothing.
- *(optional)* `extra` can be set to a string that will be added to the beginning (after the standard Python header) of any file in which there's at least one match for `grammar` (this feature is commonly used for adding in imports).

.. _pyparsing: http://pyparsing.wikispaces.com/?responseToken=0e496b5858334de54399a12b24b815040

That sounds complicated, but it's actually very simple. To start learning more, it's recommended you check out Undebt's `example patterns`_ and `pattern utilities`_.

.. _`example patterns`: examples.html
.. _`pattern utilities`: util.html

New/Advanced Style
------------------

When writing a new/advanced style pattern, you need only define one name:

- `patterns` is a list of `(grammar, replace)` tuples, where each tuple in the list is only run if the previous one succeeded

If `patterns` is defined, Undebt will ignore any definitions of `grammar`, `replace`, and `extra`. Instead, all of that information should go into the `patterns` list.

As an example, you can replicate the behavior of the old/basic style `extra` by doing the following::

    from undebt.pattern.python import HEADER

    @tokens_as_list(assert_len=1)
    def extra_replace(tokens):
        return tokens[0] + extra + "\n"

    patterns.append((HEADER, extra_replace))

Or equivalently but more succinctly::

    from undebt.pattern.interface import get_pattern_for_extra

    patterns.append(
        get_pattern_for_extra(
            extra
        )
    )
