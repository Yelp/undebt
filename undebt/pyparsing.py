# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

"""
Import from undebt.pyparsing instead of pyparsing to automatically
get the performance benefits of cPyparsing when available and fall
back to pyparsing when not.
"""

try:
    from cPyparsing import *  # NOQA
    from cPyparsing import _trim_arity  # NOQA
except ImportError:
    from pyparsing import *  # NOQA
    from pyparsing import _trim_arity  # NOQA
