# -*- coding: utf-8 -*-
"""Pattern for removing occurrences of contextlib.nested().

contextlib.nested is deprecated from 2.6 to 2.7, but plenty of code still uses
it. This refactor converts it to a regular with statement.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pyparsing import Keyword
from pyparsing import Optional
from pyparsing import ZeroOrMore

from undebt.pattern.common import COLON
from undebt.pattern.common import COMMA_IND
from undebt.pattern.common import DOT
from undebt.pattern.common import IND_RPAREN
from undebt.pattern.common import INDENT
from undebt.pattern.common import LPAREN_IND
from undebt.pattern.python import EXPR
from undebt.pattern.util import tokens_as_dict


expr_list = (
    LPAREN_IND.suppress() + EXPR
    + ZeroOrMore(COMMA_IND.suppress() + EXPR)
    + Optional(COMMA_IND.suppress()) + IND_RPAREN.suppress()
)
grammar = (
    INDENT("leading indent") + Keyword("with")
    + Optional(Keyword("contextlib") + DOT) + Keyword("nested") + expr_list("nested calls")
    + Optional(Keyword("as").suppress() + expr_list("as assignments")) + COLON
)


@tokens_as_dict(assert_keys_in=["leading indent", "nested calls", "as assignments"])
def replace(tokens):
    """
    with contextlib.nested(a, b, c) as (x, y, z):
    ->
    with a as x, \\
        b as y, \\
        c as z:
    """
    leading_indent, nested_calls = tokens["leading indent"], tokens["nested calls"]
    lw = leading_indent[1:] if leading_indent.startswith("\n") else leading_indent
    if "as assignments" in tokens:
        as_assignments = tokens["as assignments"]
        assert len(nested_calls) == len(as_assignments)
        return (
            leading_indent + "with "
            + (", \\\n" + lw + "    ").join(
                nc.strip() + " as " + aa.strip()
                for nc, aa in zip(nested_calls, as_assignments)
            ) + ":"
        )
    else:
        return (
            leading_indent + "with "
            + (", \\\n" + lw + "    ").join(
                nc.strip() for nc in nested_calls
            ) + ":"
        )
