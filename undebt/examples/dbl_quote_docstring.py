# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from undebt.pattern.common import TRIPLE_SGL_QUOTE_STRING
from undebt.pattern.util import tokens_as_list


grammar = TRIPLE_SGL_QUOTE_STRING


@tokens_as_list(assert_len=1)
def replace(tokens):
    """
    ''' --> \"\"\"
    """
    assert tokens[0][:3] == "'''" == tokens[0][-3:]
    inside_str = tokens[0][3:-3]
    if '"""' in inside_str or inside_str.startswith('"') or inside_str.endswith('"'):
        return None
    else:
        return '"""' + inside_str + '"""'
