# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys
import traceback

from undebt.cmd import logger
from undebt.cmd.logger import log
from undebt.cmd.logic import process
from undebt.pattern.interface import patterns_from_files


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
def _handle_arguments():
    parser = argparse.ArgumentParser(prog='undebt')
    parser.add_argument(
        'files', nargs='*', metavar='FILE',
        help='files to be modified; uses stdin if not passed',
    )
    parser.add_argument(
        '--pattern', '-p', metavar='PATH', action='append', required=True,
        help='paths to pattern definition files or modules',
    )
    parser.add_argument(
        '--verbose', '-v', action='store_true', default=False,
        help='verbose logging for troubleshooting',
    )
    parser.add_argument(
        '--dry-run', '-d', action='store_true', default=False,
        help='only print to stdout; do not overwrite files',
    )
    return parser.parse_args()


def _process_file(patterns, text_file, dry_run):
    log.info('undebting {}'.format(text_file))

    text = _load_text(text_file)

    try:
        result_text = process(patterns, text)
    except Exception:
        log.exception(traceback.format_exc())
        return False
    else:
        if result_text != text:
            _write_result_text(result_text, text_file, dry_run)
        return True


class _file_processor(object):
    """Must be a class so it is pickleable."""

    def __init__(self, pattern_files, dry_run):
        self.pattern_files = pattern_files
        self.dry_run = dry_run

    @_exit_fail_upon_error
    def patterns(self):
        return patterns_from_files(self.pattern_files)

    def __call__(self, text_file):
        return _process_file(self.patterns(), text_file, self.dry_run)


def main():
    """Handle and process arguments from sys.argv."""
    args = _handle_arguments()

    logger.setup(args.verbose)
    processor = _file_processor(args.pattern, args.dry_run)
    files = args.files

    if not files:
        log.info('running in stdin/stdout mode')
        processor(None)
        return

    log.info('running across {} file(s)'.format(len(files)))
    for f in files:
        processor(f)
