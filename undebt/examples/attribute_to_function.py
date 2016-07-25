# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pyparsing import Keyword
from pyparsing import ZeroOrMore

from undebt.pattern.common import BRACKETS
from undebt.pattern.common import DOT
from undebt.pattern.common import NAME
from undebt.pattern.common import PARENS
from undebt.pattern.python import ATOM_BASE
from undebt.pattern.util import condense
from undebt.pattern.util import tokens_as_list


attribute = Keyword("attribute")
grammar = (
    condense(ATOM_BASE + ZeroOrMore(DOT + ~attribute + NAME | PARENS | BRACKETS))
    + (DOT + attribute).suppress()
)


@tokens_as_list(assert_len=1)
def replace(tokens):
    """obj.attribute -> function(obj)"""
    return "function(" + tokens[0] + ")"


extra = "from function_lives_here import function"
