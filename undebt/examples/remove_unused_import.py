# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from undebt.pattern.python import HEADER
from undebt.pattern.util import tokens_as_list


grammar = HEADER


@tokens_as_list(assert_len=1)
def replace(original, location, tokens):
    header, original_without_header = tokens[0], original[len(tokens[0]):]
    if "function" in original_without_header:
        return None
    elif "from function_lives_here import function\n" in header:
        return header.replace("from function_lives_here import function\n", "")
    else:
        return None
