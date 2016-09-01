# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pyparsing import Literal

from undebt.pattern.lang.python import UNARY_OP_ATOM
from undebt.pattern.util import tokens_as_list


grammar = UNARY_OP_ATOM + Literal("<>").suppress() + UNARY_OP_ATOM


@tokens_as_list(assert_len=2)
def replace(tokens):
    """foo <> bar -> foo != bar"""
    return tokens[0] + " != " + tokens[1]
