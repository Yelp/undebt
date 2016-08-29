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
        'paths', nargs='*', metavar='PATH',
        help='paths to files or directories (searches for extension recursively) to be modified; '
        'uses stdin if not passed')
    parser.add_argument(
        '--pattern', '-p', metavar='PATH', action='append', required=True,
        help='paths to pattern definition files')
    # TODO: add --grep option. Example of usage: undebt -p <my_pattern> --grep <some string>
    parser.add_argument(
        '--extension', '-e', metavar='EXT', action='append',
        help='extensions of files to be modified when searching a directory')
    parser.add_argument(
        '--jobs', '-j', metavar='INTEGER', type=int, default=16,
        help='number of processes to run in parallel (default is 16)')
    parser.add_argument(
        '--verbose', '-v', action='store_true', default=False,
        help='verbose logging for troubleshooting')
    parser.add_argument(
        '--dry-run', '-d', action='store_true', default=False,
        help='only print to stdout; do not overwrite files')
    return parser.parse_args()


@_exit_fail_upon_error
def _fix_exts(extensions):
    if extensions is None:
        return None

    new_exts = []
    for ext in extensions:
        if ext.startswith("."):
            new_exts.append(ext[1:])
        else:
            new_exts.append(ext)
    return new_exts


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
    logger.setup()
    args = _handle_arguments()
    logger.setup(args.verbose)  # Reset logging level

    if args.jobs <= 0:
        log.error('number of processes must be > 0')
        sys.exit(1)

    processor = _file_processor(args.pattern, args.dry_run)
    files = list(_find_files(args.paths, _fix_exts(args.extension)))

    if bool(files) != bool(args.paths):
        log.error('could not find any files for the given paths and extension')
        sys.exit(1)

    if not files:  # Single process mode if stdin
        log.info('running in stdin/stdout mode')
        processor(None)

    elif len(files) == 1 or args.jobs == 1:  # Single process if only one file or only one process
        log.info('running across {} file(s) using a single process'
                 .format(len(files)))
        processor(files[0])

    else:
        process_pool = multiprocessing.Pool(args.jobs)
        try:

            result = process_pool.map_async(
                processor,
                files,
            )
            process_pool.close()

            log.info('running across {} file(s) using {} processes'
                     .format(len(files), args.jobs))

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
