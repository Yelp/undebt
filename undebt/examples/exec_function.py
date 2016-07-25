# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pyparsing import Keyword
from pyparsing import Optional

from undebt.pattern.common import COMMA
from undebt.pattern.common import INDENT
from undebt.pattern.python import ATOM
from undebt.pattern.util import tokens_as_list


grammar = (
    INDENT + Keyword("exec").suppress() + ATOM + Keyword("in").suppress() + ATOM
    + Optional(COMMA.suppress() + ATOM)
)


@tokens_as_list(assert_len_in=(3, 4))
def replace(tokens):
    """
    exec str in globals(), locals()
    ->
    exec(str, globals(), locals())
    """
    return tokens[0] + "exec(" + ", ".join(tokens[1:]) + ")"
