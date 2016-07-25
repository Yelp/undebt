# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pyparsing import Keyword
from pyparsing import ZeroOrMore

from undebt.pattern.common import BRACKETS
from undebt.pattern.common import DOT
from undebt.pattern.common import LPAREN
from undebt.pattern.common import NAME
from undebt.pattern.common import PARENS
from undebt.pattern.common import RPAREN
from undebt.pattern.python import ATOM_BASE
from undebt.pattern.util import condense
from undebt.pattern.util import tokens_as_list


method = Keyword("method")
grammar = (
    ~(Keyword("self") + DOT + method)
    + condense(ATOM_BASE + ZeroOrMore(DOT + ~method + NAME | PARENS | BRACKETS))
    + (DOT + method + LPAREN + RPAREN).suppress()
)


@tokens_as_list(assert_len=1)
def replace(tokens):
    """obj.method() -> function(obj)"""
    return "function(" + tokens[0] + ")"


extra = "from function_lives_here import function"
