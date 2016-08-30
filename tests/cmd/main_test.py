# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os.path

import mock

from undebt.cmd.main import main
from undebt.examples import method_to_function


tests_inputs_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), "inputs")

method_to_function_path = os.path.splitext(method_to_function.__file__)[0] + ".py"

method_to_function_input_path = os.path.join(tests_inputs_directory, "method_to_function_input.txt")
with open(method_to_function_input_path, "r") as f:
    method_to_function_input_contents = f.read()

method_to_function_output_path = os.path.join(tests_inputs_directory, "method_to_function_output.txt")
with open(method_to_function_output_path, "r") as f:
    method_to_function_output_contents = f.read()


def test_input_output_different():
    assert method_to_function_input_contents != method_to_function_output_contents


def _read_input_file():
    with open(method_to_function_input_path, "r+") as f:
        try:
            return f.read()
        finally:
            f.seek(0)
            f.truncate()
            f.write(method_to_function_input_contents)


def _read_output_file():
    with open(method_to_function_output_path, "r+") as f:
        try:
            return f.read()
        finally:
            f.seek(0)
            f.truncate()
            f.write(method_to_function_output_contents)


def test_single_file():
    args = ["undebt", "-p", method_to_function_path, method_to_function_input_path, "--verbose"]
    with mock.patch("sys.argv", args):
        main()
    assert _read_input_file() == method_to_function_output_contents == _read_output_file()


def test_loading_pattern_with_module_name():
    # Have to do some schenanigans here to get the module name to look like it
    # came from the project root
    module_name = 'undebt' + (
        method_to_function_path[:-3]
        .split('undebt')[-1]
        .replace('/', '.')
    )
    args = ["undebt", "-p", module_name, method_to_function_input_path, "--verbose"]
    with mock.patch("sys.argv", args):
        main()
    assert _read_input_file() == method_to_function_output_contents == _read_output_file()


def test_dry_run(capsys):
    args = ["undebt", "-p", method_to_function_path, "--dry-run", method_to_function_input_path, "--verbose"]
    with mock.patch("sys.argv", args):
        main()
    out, err = capsys.readouterr()
    assert err == '>>> {}\n'.format(method_to_function_input_path)
    assert out == method_to_function_output_contents


def test_left_unchanged():
    assert _read_input_file() == method_to_function_input_contents
    assert _read_output_file() == method_to_function_output_contents
