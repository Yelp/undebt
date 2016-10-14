# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys
import traceback

from undebt.cmd import logger
from undebt.cmd import logic
from undebt.cmd.logger import log
from undebt.pattern.interface import patterns_from_modules


def _exit_fail_upon_error(func):

    def try_except(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            log.exception(str(err))
            sys.exit(1)

    return try_except


@_exit_fail_upon_error
def _load_text(path):
    if path is None:
        file_obj = sys.stdin
    else:
        file_obj = open(path, 'r')

    try:
        return file_obj.read()
    finally:
        if path:
            file_obj.close()


@_exit_fail_upon_error
def _write_result_text(result_text, path, dry_run):
    if not dry_run and path:
        with open(path, 'w') as file_obj:
            file_obj.write(result_text)
    else:
        if path:
            print('>>> {}'.format(path), file=sys.stderr)
        sys.stdout.write(result_text)


@_exit_fail_upon_error
def _handle_arguments(args):
    parser = argparse.ArgumentParser(prog='undebt')
    parser.add_argument(
        'files', nargs='*', metavar='FILE',
        help='files to be modified; uses stdin if not passed',
    )
    parser.add_argument(
        '--pattern', '-p', metavar='MODULE', action='append', required=True,
        help='pattern definition modules',
    )
    parser.add_argument(
        '--verbose', '-v', action='store_true', default=False,
        help='verbose logging for troubleshooting',
    )
    parser.add_argument(
        '--dry-run', '-d', action='store_true', default=False,
        help='only print to stdout; do not overwrite files',
    )
    return parser.parse_args(args)


@_exit_fail_upon_error
def load_patterns(pattern_files):
    return patterns_from_modules(pattern_files)


def process(patterns, text_file, dry_run):
    log.info('undebting {}'.format(text_file))

    text = _load_text(text_file)

    try:
        result_text = logic.process(patterns, text)
    except Exception:
        log.exception(traceback.format_exc())
        return False
    else:
        if result_text != text:
            _write_result_text(result_text, text_file, dry_run)
        return True


def main(args=sys.argv[1:]):
    """Handle and process arguments from args."""
    args = _handle_arguments(args)

    logger.setup(args.verbose)
    patterns = load_patterns(args.pattern)
    files = args.files

    if not files:
        log.info('running in stdin/stdout mode')
        process(patterns, None, args.dry_run)
        return

    log.info('running across {} file(s)'.format(len(files)))
    for f in files:
        process(patterns, f, args.dry_run)
