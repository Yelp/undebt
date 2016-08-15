# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import multiprocessing
import os
import sys
import time
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
def _write_result_text(result_text, path):
    if not path:
        file_obj = sys.stdout
    else:
        file_obj = open(path, 'w')

    try:
        file_obj.write(result_text)
    finally:
        if path:
            file_obj.close()


@_exit_fail_upon_error
def _handle_arguments():
    parser = argparse.ArgumentParser(prog='undebt')
    parser.add_argument(
        '--input', '-i', metavar='path', action='append',
        help='paths to files or directories (searched recursively for extension) to be modified (if not passed uses stdin)')
    parser.add_argument(
        '--pattern', '-p', metavar='path', action='append', required=True,
        help='paths to pattern definition files')
    parser.add_argument(
        '--extension',
        '-e',
        metavar='ext',
        action='append',
        help='extensions of files to be modified when searching a directory'
        ' (exclude ".", e.g. "py" instead of ".py")')
    parser.add_argument(
        '--multiprocess', '-m', metavar='processes', type=int, default=16,
        help='number of processes to run in parallel (default is 16)')
    parser.add_argument('--verbose', action='store_true', default=False)
    return parser.parse_args()


@_exit_fail_upon_error
def _find_files(paths, extensions):
    if paths is None:
        return

    for path in paths:

        if os.path.isfile(path):
            yield path

        else:
            for root, dirs, files in os.walk(path):

                for f in files:
                    ext = os.path.splitext(f)[-1].lstrip('.')

                    if extensions is None:
                        log.error('must pass --extension when --input is a directory')
                        sys.exit(1)

                    if ext in extensions:
                        yield os.path.join(root, f)

                for d in dirs[:]:
                    if d != "." * len(d) and d.startswith("."):  # ignore .*
                        dirs.remove(d)


def _process_file(patterns, text_file):
    log.info('undebting {}'.format(text_file))

    text = _load_text(text_file)

    try:
        result_text = process(patterns, text)
    except Exception:
        log.exception(traceback.format_exc())
        return False
    else:
        _write_result_text(result_text, text_file)
        return True


class _file_processor(object):
    """Must be a class so it is pickleable."""

    def __init__(self, pattern_files):
        self.pattern_files = pattern_files

    @_exit_fail_upon_error
    def patterns(self):
        return patterns_from_files(self.pattern_files)

    def __call__(self, text_file):
        return _process_file(self.patterns(), text_file)


def main():
    """Handle and process arguments from sys.argv."""
    logger.setup()
    args = _handle_arguments()
    logger.setup(args.verbose)  # Reset logging level

    if args.multiprocess <= 0:
        log.error('number of processes must be > 0')
        sys.exit(1)

    processor = _file_processor(args.pattern)
    files = list(_find_files(args.input, args.extension))

    if bool(files) != bool(args.input):
        log.error('could not find any files for the given paths and extension')
        sys.exit(1)

    if not files:  # Single process mode if stdin
        log.info('running in stdin/stdout mode')
        processor(None)

    elif len(files) == 1 or args.multiprocess == 1:  # Single process if only one file or only one process
        log.info('running across {} file(s) using a single process'
                 .format(len(files)))
        processor(files[0])

    else:
        process_pool = multiprocessing.Pool(args.multiprocess)
        try:

            result = process_pool.map_async(
                processor,
                files,
            )
            process_pool.close()

            log.info('running across {} file(s) using {} processes'
                     .format(len(files), args.multiprocess))

            # Cannot do process_pool.wait() because it prevents KeyboardInterrupt from being sent
            # See http://stackoverflow.com/questions/1408356/keyboard-interrupts-with-pythons-multiprocessing-pool
            while not result.ready():
                time.sleep(0.01)

            if not result.successful():
                log.error('multiprocessing failed (are your replace functions pickleable?)')
                sys.exit(1)

            result = result.get()
            assert len(result) == len(files)
            if not all(result):
                log.error('failed to process {} files'
                          .format(len(result) - sum(result)))
                sys.exit(1)

        except:
            process_pool.terminate()
            raise
        finally:
            process_pool.join()
