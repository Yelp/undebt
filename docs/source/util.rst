Undebt_: Pattern Utilities
==========================

.. _Undebt: index.html
.. default-role:: code

Undebt's `undebt.pattern` package exposes various modules full of functions and grammar elements for use in writing pattern files, all documented here.

`undebt.pattern.util`
---------------------

**tokens_as_list(assert_len=None, assert_len_in=None)**

Decorator used to wrap `replace` functions that converts the parsed tokens into a list. `assert_len` checks that the tokens have exactly the given length, while `assert_len_in` checks that the length of the tokens is in the provided list.

**tokens_as_dict(assert_keys=None, assert_keys_in=None)**

Decorator used to wrap `replace` functions that converts the parsed tokens into a dictionary, with keys assigned by calling grammar elements with the desired key as the argument. `assert_keys` checks that the keys in the token dictionary are a subset of the given keys, while `assert_keys_in` checks that the given keys are a subset of the keys in the token dictionary.

**condense(item)**

Modifies a grammar element to parse to a single token instead of many different tokens by concatenating the parsed tokens together.

**addspace(item)**

Equivalent to `condense` but also adds a space delimiter in-between the concatenated tokens.

**quoted(string)**

Returns a grammar element that matches a string containing `string`.

**leading_whitespace(text)**

Returns the whitespace at the beginning of `text`.

**trailing_whitespace(text)**

Returns the whitespace at the end of `text`.

**in_string(location, code)**

Determines if, at the given location in the code, there is an enclosing non-multiline string.

**fixto(item, output)**

Modifies a grammar element to always parse to the same fixed `output`.

**debug(item)**

Modifies a grammar element to print the tokens that it matches.

**attach(item, action)**

Modifies a grammar element to parse to the result of calling `action` on the  tokens produced by that grammar element.

`undebt.pattern.common`
-----------------------

**INDENT**
Matches any amount of indentation at the start of a line.

**PARENS, BRACKETS, BRACES**
Grammar elements that match an open parenthesis / bracket / brace to the corresponding closing parenthesis / bracket / brace.

**NAME**
Grammar element that matches a variable name.

**DOTTED_NAME**
Grammar element to match either one or more `NAME` separated by `DOT`.

**NUM**
Grammar element to match a number.

**STRING**
Grammar element that matches a string.

**TRIPLE_QUOTE_STRING, TRIPLE_DBL_QUOTE_STRING, TRIPLE_SGL_QUOTE_STRING**
Grammar elements that match different types of multi-line strings.

**NL**
= `Literal("\n")`

**DOT**
= `Literal(".")`

**LPAREN**
= `Literal("(")`

**RPAREN**
= `Literal(")")`

**COMMA**
= `Literal(",")`

**COLON**
= `Literal(":")`

**COMMA_IND, LPAREN_IND, IND_RPAREN**
Same as `COMMA`, `LPAREN`, and `RPAREN`, but allow for an `INDENT` after (for `COMMA_IND` and `LPAREN_IND`) or before (for `IND_RPAREN`).

**LINE_START**
Matches the start of a line, either after a new line, or at the start of the file.

**NO_BS_NL**
Matches a new line not preceded by a backslash.

**START_OF_FILE**
Grammar element that only matches at the very beginning of the file.

**END_OF_FILE**
Grammar element that only matches at the very end of the file.

**SKIP_TO_TEXT**
Skips parsing position to the next non-whitespace character. To see the skipped text in a token, use `originalTextFor(PREVIOUS_GRAMMAR_ELEMENT + SKIP_TO_TEXT)` where `PREVIOUS_GRAMMAR_ELEMENT` is just whatever comes before `SKIP_TO_TEXT` in your grammar.

**SKIP_TO_TEXT_OR_NL**
Same as `SKIP_TO_TEXT`, but won't skip over new lines.

**ANY_CHAR**
Grammar element that matches any one character, including new lines, but not  non-newline whitespace. To exclude newlines, just do `~NL + ANY_CHAR`.

**WHITE**
Normally, whitespace between grammar elements is ignored when they are added together. Put `WHITE` in-between to capture that whitespace as a token.

**NL_WHITE**
Same as `WHITE` but also matches new lines.

`undebt.pattern.python`
-----------------------

**EXPR**
Matches any valid Python expression.

**EXPR_LIST, EXPR_IND_LIST**
Matches one or more `EXPR` separated by `COMMA` for `EXPR_LIST` or `COMMA_IND` for `EXPR_IND_LIST`.

**ATOM**
Matches a single valid Python atom (that is, an expression without operators).

**TRAILER**
Matches a valid Python trailer (attribute access, function call, indexing, etc.).

**TRAILERS**
Matches any number of `TRAILER`.

**ATOM_BASE**
Matches an `ATOM` without any `TRAILERS` attached to it.

**OP**
Matches any valid Python operator.

**BINARY_OP**
Matches a valid Python binary operator.

**ASSIGN_OP**
Matches a valid Python assignment operator.

**UNARY_OP**
Matches a valid Python unary operator.

**UNARY_OP_ATOM**
Matches an `ATOM` potentially preceded by unary operator(s).

**HEADER**
Matches imports, comments, and strings at the start of a file. Used to determine where to insert the basic style `extra`.

`undebt.pattern.interface`
--------------------------

**get_pattern_for_extra(extra)**

Returns a `(grammar, replace)` tuple describing a pattern to insert `extra` after `undebt.pattern.python.HEADER`.

**get_patterns(*pattern_modules)**

Returns a list containing a advanced style `patterns` list for each pattern module in `pattern_modules`. The resulting list can be passed to `undebt.cmd.logic.process`.

`undebt.cmd.logic`
------------------

**process(patterns, text)**

Where `patterns` is a list of advanced style `patterns` lists, applies the specified patterns to the given text and returns the transformed version. Usually used in conjunction with `undebt.pattern.interface.get_patterns`.
