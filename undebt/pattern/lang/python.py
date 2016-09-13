# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pyparsing import Combine
from pyparsing import Keyword
from pyparsing import Literal
from pyparsing import OneOrMore
from pyparsing import Optional
from pyparsing import originalTextFor
from pyparsing import pythonStyleComment
from pyparsing import SkipTo
from pyparsing import Word
from pyparsing import ZeroOrMore

from undebt.pattern.common import BRACES
from undebt.pattern.common import BRACKETS
from undebt.pattern.common import COMMA
from undebt.pattern.common import COMMA_IND
from undebt.pattern.common import DOT
from undebt.pattern.common import NAME
from undebt.pattern.common import NL
from undebt.pattern.common import NO_BS_NL
from undebt.pattern.common import NUM
from undebt.pattern.common import PARENS
from undebt.pattern.common import SKIP_TO_TEXT
from undebt.pattern.common import START_OF_FILE
from undebt.pattern.common import STRING
from undebt.pattern.util import addspace
from undebt.pattern.util import condense


ASSIGN_OP = Combine((Word("~%^&*-+|/") | ~Literal("==")) + Literal("="))


UNARY_OP = addspace(OneOrMore(
    Word("~-+")
    | Keyword("not")
))


BINARY_OP = ~ASSIGN_OP + (
    Word("!%^&*-+=|/<>")
    | Keyword("and")
    | Keyword("or")
    | addspace(OneOrMore(
        Keyword("is")
        | Keyword("not")
        | Keyword("in")
    ))
)


OP = ASSIGN_OP | UNARY_OP | BINARY_OP


TRAILER = DOT + NAME | PARENS | BRACKETS
TRAILERS = condense(ZeroOrMore(TRAILER))


ATOM_BASE = NAME | NUM | PARENS | BRACKETS | BRACES | STRING
ATOM = condense(ATOM_BASE + TRAILERS)
UNARY_OP_ATOM = addspace(Optional(UNARY_OP) + ATOM)


EXPR = addspace(UNARY_OP_ATOM + ZeroOrMore(BINARY_OP + UNARY_OP_ATOM))
EXPR_LIST = condense(EXPR + ZeroOrMore(addspace(COMMA + EXPR)) + Optional(COMMA))
EXPR_IND_LIST = originalTextFor(EXPR + ZeroOrMore(COMMA_IND + EXPR) + Optional(COMMA_IND))


PARAM = condense(Optional(Word("*") | NAME + Literal("=")) + EXPR)
PARAMS = originalTextFor(PARAM + ZeroOrMore(COMMA_IND + PARAM) + Optional(COMMA_IND))


HEADER = originalTextFor(START_OF_FILE + ZeroOrMore(SKIP_TO_TEXT + (
    STRING
    | pythonStyleComment
    | Optional(Keyword("from") + SkipTo("import")) + Keyword("import") + (PARENS | SkipTo(NO_BS_NL))
) + NL))
