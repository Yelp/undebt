# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os.path

import mock

from undebt.cmd import logic
from undebt.cmd import main
from undebt.cmd.main import _exit_fail_upon_error
from undebt.cmd.main import _load_text
from undebt.cmd.main import _write_result_text
from undebt.examples import method_to_function


tests_inputs_directory = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "inputs",
)

method_to_function_path = os.path.splitext(
    method_to_function.__file__
)[0] + ".py"

method_to_function_input_path = os.path.join(
    tests_inputs_directory,
    "method_to_function_input.txt",
)
with open(method_to_function_input_path, "r") as f:
    method_to_function_input_contents = f.read()

method_to_function_output_path = os.path.join(
    tests_inputs_directory,
    "method_to_function_output.txt",
)
with open(method_to_function_output_path, "r") as f:
    method_to_function_output_contents = f.read()


def test_input_output_different():
    assert (
        method_to_function_input_contents != method_to_function_output_contents
    )


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


@mock.patch('undebt.cmd.main.sys.exit')
def test_exit_fail_upon_error_with_exception(mock_exit):

    @_exit_fail_upon_error
    def fake_func():
        raise Exception('fake exception')

    fake_func()
    mock_exit.assert_called_once_with(1)


@mock.patch('undebt.cmd.main.sys.stdin')
def test_load_text_is_none(mock_stdin):
    assert _load_text(None) == mock_stdin.read.return_value


@mock.patch('undebt.cmd.main.sys.stdout')
def test_write_text_file_dry_run_with_path(mock_stdout):
    fake_result_text = mock.Mock()
    _write_result_text(
        result_text=fake_result_text,
        path=None,
        dry_run=False,
    )
    mock_stdout.write.assert_called_once_with(fake_result_text)


@mock.patch('undebt.cmd.main._load_text')
@mock.patch('undebt.cmd.logic.process')
def test_process_file_with_exception(mock_process, mock_load_text):
    fake_patterns = mock.MagicMock()
    fake_text_file = mock.Mock()
    mock_process.side_effect = Exception('fake exception')

    assert main.process(
        patterns=fake_patterns,
        text_file=fake_text_file,
        dry_run=False,
    ) is False


@mock.patch('undebt.cmd.main._load_text')
@mock.patch('undebt.cmd.logic.process')
def test_process_file_raises_exception(mock_process, mock_load_text):
    fake_patterns = mock.MagicMock()
    fake_text_file = mock.Mock()
    mock_load_text.return_value = 'text does not change after process'
    mock_process.return_value = 'text does not change after process'

    assert main.process(
        patterns=fake_patterns,
        text_file=fake_text_file,
        dry_run=False,
    ) is True


@mock.patch('undebt.cmd.main.load_patterns')
@mock.patch('undebt.cmd.main.process')
def test_no_file(mock_process, mock_load_patterns):
    fake_patterns = mock.MagicMock()
    mock_load_patterns.return_value = fake_patterns
    args = ['-p', 'blah']
    main.main(args)
    mock_process.assert_called_once_with(fake_patterns, None, False)


def test_single_file():
    args = [
        "-p",
        method_to_function.__name__,
        method_to_function_input_path,
        "--verbose",
    ]
    main.main(args)
    assert (
        _read_input_file() ==
        method_to_function_output_contents ==
        _read_output_file()
    )


def test_loading_pattern_with_module_name():
    args = [
        "-p",
        method_to_function.__name__,
        method_to_function_input_path,
        "--verbose",
    ]
    main.main(args)
    assert (
        _read_input_file() ==
        method_to_function_output_contents ==
        _read_output_file()
    )


def test_dry_run(capsys):
    args = [
        "-p",
        method_to_function.__name__,
        "--dry-run",
        method_to_function_input_path,
        "--verbose",
    ]
    main.main(args)
    out, err = capsys.readouterr()
    assert err == '>>> {}\n'.format(method_to_function_input_path)
    assert out == method_to_function_output_contents


def test_left_unchanged():
    assert _read_input_file() == method_to_function_input_contents
    assert _read_output_file() == method_to_function_output_contents
