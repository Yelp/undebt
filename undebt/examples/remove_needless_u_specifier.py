# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pyparsing import Keyword
from pyparsing import Literal
from pyparsing import Optional
from pyparsing import originalTextFor
from pyparsing import ZeroOrMore

from undebt.pattern.common import COMMA
from undebt.pattern.common import NAME
from undebt.pattern.common import STRING
from undebt.pattern.util import condense
from undebt.pattern.util import tokens_as_list


unicode_literals = Keyword("unicode_literals")
non_unicode_literals_name = ~unicode_literals + NAME
import_grammar = originalTextFor(
    Keyword("from") + Keyword("__future__") + Keyword("import")
    + ZeroOrMore(non_unicode_literals_name + COMMA)
    + unicode_literals
    + ZeroOrMore(COMMA + non_unicode_literals_name)
    + Optional(COMMA)
)


u_string_grammar = Literal("u").suppress() + condense(Optional(Literal("r")) + STRING)


@tokens_as_list(assert_len=1)
def identity_replace(tokens):
    return tokens[0]


patterns = [
    # first, check to see if from __future__ import unicode_literals exists
    (import_grammar, identity_replace),
    # if it does, then find u strings and return them with the u suppressed
    (u_string_grammar, identity_replace),
]
