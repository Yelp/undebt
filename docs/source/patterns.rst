Undebt_: Pattern Files
======================

.. _Undebt: index.html
.. default-role:: code

Undebt requires a pattern file that describes what to replace and how to replace it. There are two different ways to write pattern files: basic style, and advanced style. Unless you know you need multi-pass parsing, you should use basic style by default.

Basic Style
-----------

If you don't know what style you should be using, you should be using basic style. When writing a basic style pattern, you must define the following names in your pattern file:

- `grammar` defines what pattern you want to replace, and must be a pyparsing_ grammar object.
- `replace` is a function of one argument, the tokens produced by `grammar`, that returns the string they should be replaced with, or `None` to do nothing (this is the single-argument form—multi-argument is also allowed as documented `below`_).
- *(optional)* `extra` can be set to a string that will be added to the beginning (after the standard Python header) of any file in which there's at least one match for `grammar` and in which `extra` does not already appear in the header (this feature is commonly used for adding in imports).

.. _below: #multi-argument-replace
.. _pyparsing: http://pyparsing.wikispaces.com/?responseToken=0e496b5858334de54399a12b24b815040

That sounds complicated, but it's actually very simple. To start learning more, it's recommended you check out Undebt's `example patterns`_ and `pattern utilities`_.

.. _`example patterns`: examples.html
.. _`pattern utilities`: util.html

Advanced Style
--------------

Unlike basic style, advanced style allows you to use custom multi-pass parsing—if that's not something you need, you should use basic style. When writing an advanced style pattern, you need only define one name:

- `patterns` is a list of `(grammar, replace)` tuples, where each tuple in the list is only run if the previous one succeeded

If `patterns` is defined, Undebt will ignore any definitions of `grammar`, `replace`, and `extra`. Instead, all of that information should go into the `patterns` list.

As an example, you can replicate the behavior of the basic style `extra` by doing the following::

    from undebt.pattern.lang.python import HEADER

    @tokens_as_list(assert_len=1)
    def extra_replace(tokens):
        if extra not in tokens[0]:
            return tokens[0] + extra + "\n"
        else:
            return None

    patterns.append((HEADER, extra_replace))

Or equivalently but more succinctly::

    from undebt.pattern.interface import get_pattern_for_extra

    patterns.append(
        get_pattern_for_extra(
            extra
        )
    )

Multi-Argument Replace
----------------------

In both styles, when writing a `replace` function, it is sometimes useful to have access to the parsing location in the file and/or the text of the original file. If your `replace` function takes two arguments, it will be passed `location, tokens`, and for three arguments, it will get `text, location, tokens`. This will work even if you are using one of the `tokens_as_list` or `tokens_as_dict` decorators.
