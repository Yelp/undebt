# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from undebt.cmd.logic import process
from undebt.examples import sqla_count
from undebt.pattern.interface import get_patterns
from undebt.pattern.testing import assert_transform


def test_one_liner():
    assert_transform(
        sqla_count,
        'session.query(x).filter(y).count()',
        ['session.query(sqlalchemy.func.count()).filter(y).scalar()'],
    )


def test_multi_line():
    text = """session.query(
        mu,
    ).filter(
        mu.t > abc,
        mu.id == id,
    ).count()"""
    expected = """session.query(
        sqlalchemy.func.count(),
    ).filter(
        mu.t > abc,
        mu.id == id,
    ).scalar()"""
    assert_transform(sqla_count, text, [expected])


def test_actual_code():
    text = """something before
        x = session.query(
            mr,
        ).filter(
            mr.t < xyz,
        ).count()
    something after
    """
    expected = """session.query(
            sqlalchemy.func.count(),
        ).filter(
            mr.t < xyz,
        ).scalar()"""
    assert_transform(sqla_count, text, [expected])


def test_sqla_count():
    patterns = get_patterns(sqla_count)
    text = """
    session.query(
        derp,
    ).filter(
        herp,
    ).count()
"""
    assert process(patterns, text) == (
        """import sqlalchemy

    session.query(
        sqlalchemy.func.count(),
    ).filter(
        herp,
    ).scalar()
""")
