# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pyparsing import Combine
from pyparsing import hexnums
from pyparsing import Literal
from pyparsing import Word

from undebt.pattern.util import tokens_as_list

grammar = Combine(Literal("0x").suppress() + Word(hexnums))


@tokens_as_list(assert_len=1)
def replace(tokens):
    """0x00000001 --> 1 << 0"""
    flag = int(tokens[0], 16)
    shift = flag.bit_length() - 1
    if shift >= 0 and 1 << shift == flag:
        return "1 << " + str(shift)
    else:
        return None
