# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging


log = logging.getLogger('undebt')

initialized = False


def setup(verbose=False):

    if verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.ERROR)

    global initialized
    if not initialized:
        log_stream = logging.StreamHandler()
        log_stream.setFormatter(logging.Formatter("%(asctime)s - %(name)s[%(process)d] - %(levelname)s - %(message)s"))
        log.addHandler(log_stream)

    initialized = True
