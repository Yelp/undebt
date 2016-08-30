# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

import mock

from undebt.cmd.logger import setup


@mock.patch('undebt.cmd.logger.log')
def test_setup_verbose_false(mock_log):
    setup(verbose=False)
    mock_log.setLevel.assert_called_once_with(logging.ERROR)
