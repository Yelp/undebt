# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pyparsing import Keyword
from pyparsing import Literal

from undebt.pattern.common import DOT
from undebt.pattern.common import LPAREN
from undebt.pattern.common import PARENS
from undebt.pattern.common import RPAREN
from undebt.pattern.util import leading_whitespace
from undebt.pattern.util import tokens_as_dict
from undebt.pattern.util import trailing_whitespace


grammar = (
    Keyword("session") + DOT + Keyword("query") + PARENS + DOT + Literal("filter")
    + PARENS("filter call")
    + DOT + Keyword("count") + LPAREN + RPAREN
)


@tokens_as_dict(assert_keys=["filter call"])
def replace(tokens):
    """
    session.query(
        ...
    ).filter(
        ...
    ).count()
    ->
    session.query(
        sqlalchemy.func.count()
    ).filter(
        ...
    ).scalar()
    """
    filter_call = tokens["filter call"]
    lw, tw = leading_whitespace(filter_call[1:]), trailing_whitespace(filter_call[:-1])
    return (
        "session.query(" +
        lw + "sqlalchemy.func.count()" + ("," if "\n" in tw else "") + tw +
        ").filter" +
        filter_call +
        ".scalar()"
    )


extra = "import sqlalchemy"
