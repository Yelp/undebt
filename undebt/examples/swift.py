# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from undebt.pattern.common import NAME
from undebt.pattern.lang.python import EXPR
from undebt.pattern.util import condense
from undebt.pattern.util import tokens_as_dict
from undebt.pyparsing import delimitedList
from undebt.pyparsing import Keyword
from undebt.pyparsing import Literal
from undebt.pyparsing import SkipTo


if_ = Keyword("if")
let = Keyword("let")
where = Keyword("where")
eq = Literal("=")

assign = condense(NAME + eq + EXPR)

grammar = (
    if_ + let + delimitedList(assign)("let-bindings")
    + where + SkipTo("{")("where-clause")
)


@tokens_as_dict(assert_keys=["let-bindings", "where-clause"])
def replace(tokens):
    assigns = tokens["let-bindings"]
    cond = tokens['where-clause']

    def pretty_assign(assign):
        op = assign.index("=")
        l, r = assign[:op], assign[op + 1:]
        return "{0} = {1}".format(l, r)

    new_assigns = ", let ".join(map(pretty_assign, assigns))
    return "if let " + new_assigns + ", " + cond + "{"
