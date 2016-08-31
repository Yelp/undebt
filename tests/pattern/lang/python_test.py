# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from undebt.pattern.lang.python import ATOM
from undebt.pattern.lang.python import BINARY_OP
from undebt.pattern.lang.python import EXPR
from undebt.pattern.lang.python import EXPR_IND_LIST
from undebt.pattern.lang.python import EXPR_LIST
from undebt.pattern.lang.python import HEADER
from undebt.pattern.lang.python import OP
from undebt.pattern.testing import assert_parse


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


def test_BINARY_OP():
    assert_parse(
        grammar=BINARY_OP,
        text="==",
        tokens_list=[["=="]],
        interval_list=[(0, 2)],
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


def test_EXPR_LIST():
    assert_parse(
        grammar=EXPR_LIST,
        text="""
        derp + herp, herp.a.derp - 1, herp[derp],
        """,
        tokens_list=[
            ["derp + herp, herp.a.derp - 1, herp[derp],"],
        ],
        interval_list=[
            (9, 50),
        ],
    )


def test_EXPR_IND_LIST():
    assert_parse(
        grammar=EXPR_IND_LIST,
        text="""
        derp + herp,
        herp.a.derp - 1,
        herp[derp]
        """,
        tokens_list=[
            ["""derp + herp,
        herp.a.derp - 1,
        herp[derp]"""],
        ],
        interval_list=[
            (9, 65),
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
from foo import *
from foo import (
    bar,
    baz as foobar)
from .bar import *
from .bar import alpha, beta
from . import baz


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
from foo import *
from foo import (
    bar,
    baz as foobar)
from .bar import *
from .bar import alpha, beta
from . import baz
''']],
        interval_list=[
            (0, 295),
        ],
    )
