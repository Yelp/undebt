# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from undebt.pattern.common import ANY_CHAR
from undebt.pattern.common import END_OF_FILE
from undebt.pattern.common import NL
from undebt.pattern.util import tokens_as_list


grammar = ~NL + ANY_CHAR + END_OF_FILE


@tokens_as_list(assert_len=1)
def replace(tokens):
    # tokens = [ANY_CHAR]
    return tokens[0] + "\n"
