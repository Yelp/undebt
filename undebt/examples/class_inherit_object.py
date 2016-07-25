# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pyparsing import Keyword
from pyparsing import Optional

from undebt.pattern.common import COLON
from undebt.pattern.common import INDENT
from undebt.pattern.common import LPAREN
from undebt.pattern.common import NAME
from undebt.pattern.common import RPAREN
from undebt.pattern.util import tokens_as_list


grammar = INDENT + Keyword("class").suppress() + NAME + (Optional(LPAREN + RPAREN) + COLON).suppress()


@tokens_as_list(assert_len=2)
def replace(tokens):
    return tokens[0] + "class " + tokens[1] + "(object):"
