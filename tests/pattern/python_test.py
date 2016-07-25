# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tests import assert_parse
from undebt.pattern.python import ATOM
from undebt.pattern.python import EXPR
from undebt.pattern.python import HEADER
from undebt.pattern.python import OP


def test_OP():
    assert_parse(
        grammar=OP,
        text="""
        abc += 25 // 3 * 2 - 4 != 10
        """,
        tokens_list=[
            ["+="],
            ["//"],
            ["*"],
            ["-"],
            ["!="],
        ],
        interval_list=[
            (13, 15),
            (19, 21),
            (24, 25),
            (28, 29),
            (32, 34),
        ],
    )


def test_ATOM():
    assert_parse(
        grammar=ATOM,
        text="""
        self.derp(herp)['derp'] + {'herp': 'derp'}.get()
        """,
        tokens_list=[
            ["self.derp(herp)['derp']"],
            ["{'herp': 'derp'}.get()"],
        ],
        interval_list=[
            (9, 32),
            (35, 57),
        ],
    )


def test_EXPR():
    assert_parse(
        grammar=EXPR,
        text="""
        self.derp(herp)['derp'] + {'herp': 'derp'}.get()
        """,
        tokens_list=[
            ["self.derp(herp)['derp'] + {'herp': 'derp'}.get()"],
        ],
        interval_list=[
            (9, 57),
        ],
    )


def test_HEADER():
    assert_parse(
        grammar=HEADER,
        text='''#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""doc"""

from __future__ import herpaderp

import start
from derp import herp
from herpderp import herp, \\
 derp

first
second
        ''',
        tokens_list=[['''#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""doc"""

from __future__ import herpaderp

import start
from derp import herp
from herpderp import herp, \\
 derp
''']],
        interval_list=[
            (0, 162),
        ],
    )
