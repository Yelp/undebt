# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re

from pyparsing import CharsNotIn
from pyparsing import Literal
from pyparsing import nestedExpr
from pyparsing import Optional
from pyparsing import originalTextFor
from pyparsing import quotedString
from pyparsing import Regex
from pyparsing import SkipTo
from pyparsing import StringEnd
from pyparsing import StringStart
from pyparsing import Word
from pyparsing import ZeroOrMore

from undebt.pattern import WHITESPACE_CHARS
from undebt.pattern import WHITESPACE_OR_NL_CHARS
from undebt.pattern.util import condense
from undebt.pattern.util import fixto


ANY_CHAR = Regex(r".", re.DOTALL)


START_OF_FILE = StringStart().suppress()
END_OF_FILE = StringEnd().suppress()


NL = Literal("\n")
DOT = Literal(".")
LPAREN = Literal("(")
RPAREN = Literal(")")
COMMA = Literal(",")
COLON = Literal(":")


LINE_START = NL | fixto(START_OF_FILE, "")
NO_BS_NL = Regex(r"(?<!\\)").suppress() + NL


SKIP_TO_TEXT = SkipTo(CharsNotIn(WHITESPACE_OR_NL_CHARS))
SKIP_TO_TEXT_OR_NL = SkipTo(CharsNotIn(WHITESPACE_CHARS))
INDENT = originalTextFor(LINE_START + SKIP_TO_TEXT_OR_NL)


WHITE = ~START_OF_FILE + Word(WHITESPACE_CHARS).setWhitespaceChars("")
NL_WHITE = ~START_OF_FILE + Word(WHITESPACE_OR_NL_CHARS).setWhitespaceChars("")


COMMA_IND = condense(COMMA + Optional(INDENT))
LPAREN_IND = condense(LPAREN + Optional(INDENT))
IND_RPAREN = condense(Optional(INDENT) + RPAREN)


def _untouched_string(quote):
    """Matches a string from quote to quote. Does not handle escapes."""
    return originalTextFor(Literal(quote) + SkipTo(quote) + Literal(quote))


TRIPLE_DBL_QUOTE_STRING = _untouched_string('"""')
TRIPLE_SGL_QUOTE_STRING = _untouched_string("'''")
TRIPLE_QUOTE_STRING = TRIPLE_DBL_QUOTE_STRING | TRIPLE_SGL_QUOTE_STRING
STRING = TRIPLE_QUOTE_STRING | quotedString


def _untouched_nested_expr(left, right):
    """Matches a nested expression without changing the original text."""
    return originalTextFor(nestedExpr(left, right, ignoreExpr=NL | STRING))


PARENS = _untouched_nested_expr("(", ")")
BRACKETS = _untouched_nested_expr("[", "]")
BRACES = _untouched_nested_expr("{", "}")


NAME = Regex(r"\b(?![0-9])\w+\b")
DOTTED_NAME = condense(NAME + ZeroOrMore(DOT + NAME))


NUM = ~NAME + Word("box0123456789.eEjJ")
