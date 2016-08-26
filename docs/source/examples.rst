Undebt_: Examples
=================

.. _Undebt: index.html
.. default-role:: code

The `undebt.examples`_ package contains various example pattern files. These example patterns can either simply be used as they are to make use of the transformation they describe, or used as templates to `build your own pattern files`_.

.. _`undebt.examples`: https://github.com/Yelp/undebt/tree/master/undebt/examples
.. _`build your own pattern files`: patterns.html

`undebt.examples.nl_at_eof`
---------------------------
(`Source
<https://github.com/Yelp/undebt/blob/master/undebt/examples/nl_at_eof.py>`_)

A toy example to add a new line (`"\n"`) to the end of files that lack one.

Example of:

- use of the `tokens_as_list` decorator to define a `replace` function with assert checks
- negative lookahead using the `~` operator
- match any character with `ANY_CHAR`
- match the end of a file with `END_OF_FILE`

`undebt.examples.dbl_quote_docstring`
-------------------------------------
(`Source
<https://github.com/Yelp/undebt/blob/master/undebt/examples/dbl_quote_docstring.py>`_)

Changes all `'''` strings that can be changed to `"""` strings.

Example of:

- return `None` from `replace` to do nothing
- match a `'''` string using `TRIPLE_SGL_QUOTE_STRING`

`undebt.examples.class_inherit_object`
--------------------------------------
(`Source
<https://github.com/Yelp/undebt/blob/master/undebt/examples/class_inherit_object.py>`_)

Changes classes that inherit from nothing to inherit from `object`, which makes sure they behave as Python 3 new-style classes instead of Python 2 old-style classes.

Example of:

- `Optional` to optionally match something
- `.suppress` method to prevent an object from appearing in the parsed tokens
- `Keyword` to match an individual word
- `INDENT` to match the beginning of a line and any leading whitespace
- `NAME` to match any variable name

`undebt.examples.hex_to_bitshift`
---------------------------------
(`Source
<https://github.com/Yelp/undebt/blob/master/undebt/examples/hex_to_bitshift.py>`_)

Replaces hex flags with bitshift flags.

Example of:

- `Literal` to match a specific literal
- `Combine` to match a series of tokens without any whitespace in-between
- `Word` to match a word made up of a set of characters

`undebt.examples.exec_function`
-------------------------------
(`Source
<https://github.com/Yelp/undebt/blob/master/undebt/examples/exec_function.py>`_)

Changes instances of the Python 2 style `exec code in globals, locals` exec statement to the universal Python style `exec(code, globals, locals)` (which will work on Python 2.7 and Python 3).

Example of:

- using `tokens_as_list` to assert multiple possible token list lengths
- `ATOM` to match a Python atom

`undebt.examples.attribute_to_function`
---------------------------------------
(`Source
<https://github.com/Yelp/undebt/blob/master/undebt/examples/attribute_to_function.py>`_)

Transforms uses of `.attribute` into calls to `function`, and adds `from function_lives_here import function` whenever an instance of `function` is added.

Example of:

- use of `extra` to add an import statement
- multiple possible patterns using the `|` operator
- `ZeroOrMore` to match any number of a pattern
- `PARENS, BRACKETS` to match anything inside matching parentheses and brackets
- `ATOM_BASE` to match a trailerless Python atom

`undebt.examples.method_to_function`
------------------------------------
(`Source
<https://github.com/Yelp/undebt/blob/master/undebt/examples/method_to_function.py>`_)

Slightly more complicated version of `attribute_to_function` that finds a method call instead of an attribute access, and makes sure that method call is not on `self`.

`undebt.examples.sqla_count`
----------------------------
(`Source
<https://github.com/Yelp/undebt/blob/master/undebt/examples/sqla_count.py>`_)

Transforms inefficient SQL alchemy `.count()` queries into more efficient `.scalar()` queries that don't create a sub query.

Example of:

- use of the `tokens_as_dict` decorator to define a `replace` function with assert checks
- grammar element function calling to label tokens in the resulting `tokens_as_dict` dictionary
- using `leading_whitespace` and `trailing_whitespace` to extract whitespace in a `replace` function

`undebt.examples.remove_unused_import`
--------------------------------------
(`Source
<https://github.com/Yelp/undebt/blob/master/undebt/examples/remove_unused_import.py>`_)

Removes `from function_lives_here import function` if `function` does not appear anywhere else in the file.

Example of:

- using a multi-argument `replace` function
- using `HEADER` to analyze the header of a Python file

`undebt.examples.contextlib_nested`
-----------------------------------
(`Source
<https://github.com/Yelp/undebt/blob/master/undebt/examples/contextlib_nested.py>`_)

Transforms uses of `contextlib.nested` into multiple clauses in a `with` statement. Respects usage with `as` and without `as`.

Example of:

- using `tokens_as_dict` to assert multiple possible dictionary keys
- `EXPR` to match a Python expression
- `COMMA_IND, LPAREN_IND, IND_RPAREN` to match optional indentation at particular points

`undebt.examples.remove_needless_u_specifier`
---------------------------------------------
(`Source
<https://github.com/Yelp/undebt/blob/master/undebt/examples/remove_needless_u_specifier.py>`_)

In files where `from __future__ import unicode_literals` appears, removes unnecessary `u` before strings.

Example of:

- an advanced style pattern file making use of multi-pass parsing
- using `in_string` to determine if the match location is inside of a string
- `originalTextFor` to make grammar elements parse to the original text that matched them
- `STRING` to match any valid string

`undebt.examples.swift`
-----------------------------------
(`Source
<https://github.com/Yelp/undebt/blob/master/undebt/examples/swift.py>`_)

Transforms uses of `if let where` from Swift 2.2 to the updated syntax in Swift
3.0.

Example of:

- using Undebt to transform a language that isn't Python
*Note: It's possible that the `EXPR` grammar element used won't match all Swift expressions; if you are concerned about this, you should define a custom `EXPR` corresponding to the syntax of a Swift expression.*
