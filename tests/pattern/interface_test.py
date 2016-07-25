# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from undebt.examples import attribute_to_function
from undebt.pattern.interface import get_patterns
from undebt.pattern.python import HEADER


def test_get_patterns():
    # patterns = [[(grammar, replace), (HEADER, extra_replace)]]
    patterns = get_patterns(attribute_to_function)
    [patternset] = patterns
    [pattern1, pattern2] = patternset
    (grammar1, replace1) = pattern1
    (grammar2, replace2) = pattern2
    assert grammar2 is HEADER
