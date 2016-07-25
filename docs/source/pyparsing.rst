Undebt_: Using `pyparsing`
==========================

.. _Undebt: index.html
.. default-role:: code

While Undebt's `parsing utilities`_ are very helpful and provide much of the necessary functionality for writing a `grammar`, all of the objects are `pyparsing`_ objects, and thus it is often necessary and/or useful to use `pyparsing` utilities.

.. _`pyparsing`: http://pyparsing.wikispaces.com/
.. _`parsing utilities`: util.html

While the `official pyparsing documentation`_ is a great resource, most of the more advanced utilities there will usually not be necessary. This documentation is an overview of those that are most likely to be useful.

.. _`official pyparsing documentation`: https://pythonhosted.org/pyparsing/

Operators
---------

**+: And**

Adding two grammar elements produces a new grammar element that matches the first one, then the second one, with optional intervening whitespace.

**|: Or**

Oring two grammar elements produces a new grammar element that attempts to match the first one, then if that fails, attempts to match the second one.

**~: Negative Lookahead**

Inverting a grammar element produces a new grammar element that produces no tokens and matches only if the inverted grammar doesn't match. Using a negative lookahead also doesn't advance the current parsing position.

**^: Match Longest**

Similar to `|`, but matches the longest of the grammar elements that match, instead of the first grammar element that matches.

Functions
---------

**Literal(str)**

Creates a grammar element that matches `str` exactly.

**Keyword(str)**

Creates a grammar element that matches `str` only if it is surrounded by non-letters.

**Optional(...)**

Creates a grammar element that matches zero or one of the contained grammar element.

**ZeroOrMore(...)**

Creates a grammar element that matches zero or more of the contained grammar element.

**OneOrMore(...)**

Creates a grammar element that matches one or more of the contained grammar element.

**originalTextFor(...)**

Modifies a grammar element to produce only a single token that is the original text that was matched by that grammar element.

**Word(charset)**

Creates a grammar element that matches a word made of characters in `charset`.

**SkipTo(...)**

Skips parsing position to the next match for the contained objects.

**Combine(...)**

Forces any grammar elements added together inside of `Combine` to not match intervening whitespace and produce only a single token.

**Regex(str)**

Creates a grammar element that matches `str` as a regular expression.
