# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from undebt.pattern.common import COMMA
from undebt.pattern.common import NAME
from undebt.pattern.common import STRING
from undebt.pattern.util import condense
from undebt.pattern.util import in_string
from undebt.pattern.util import tokens_as_list
from undebt.pyparsing import Keyword
from undebt.pyparsing import Literal
from undebt.pyparsing import Optional
from undebt.pyparsing import originalTextFor
from undebt.pyparsing import ZeroOrMore


unicode_literals = Keyword("unicode_literals")
non_unicode_literals_name = ~unicode_literals + NAME
import_grammar = originalTextFor(
    Keyword("from") + Keyword("__future__") + Keyword("import")
    + ZeroOrMore(non_unicode_literals_name + COMMA)
    + unicode_literals
    + ZeroOrMore(COMMA + non_unicode_literals_name)
    + Optional(COMMA)
)


@tokens_as_list(assert_len=1)
def identity_replace(tokens):
    return tokens[0]


u_string_grammar = Literal("u").suppress() + condense(Optional(Literal("r")) + STRING)


@tokens_as_list(assert_len=1)
def u_string_replace(original, location, tokens):
    if in_string(location, original):
        return None
    else:
        return tokens[0]


patterns = [
    # first, check to see if from __future__ import unicode_literals exists
    (import_grammar, identity_replace),
    # if it does, then find u strings and return them with the u suppressed
    (u_string_grammar, u_string_replace),
]
