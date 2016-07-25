# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from undebt.cmd.logger import log
from undebt.pattern.interface import parse_grammar


def process(patterns, text):
    """Return text modified by patterns."""

    for i in range(len(patterns)):
        if isinstance(patterns[i], tuple):
            inner_patterns = [patterns[i]]
        else:
            inner_patterns = patterns[i]

        found = []
        for grammar, replace in inner_patterns:

            results = parse_grammar(grammar, text)
            if not results:
                break
            else:
                found.append(len(results))
                text = _transform_results(replace, results, text)

        if found:
            log.info('=> pattern {} found {} time(s) in {} pass(es)'
                     .format(i + 1, sum(found), len(found)))
        else:
            log.info('__ pattern {} not found'
                     .format(i + 1))

    return text


def _transform_results(replace, results, text):
    found_tokens = [tokens for tokens, _, _ in results]
    intervals = [(start, end) for _, start, end in results]
    new_strings = [replace(tokens) for tokens in found_tokens]

    _no_replace_to_none(new_strings, intervals)
    return _replace_with(text, new_strings, intervals)


def _no_replace_to_none(new_strings, intervals):
    assert len(new_strings) == len(intervals)
    i = 0
    while i < len(new_strings):
        if new_strings[i] is None:
            new_strings.pop(i)
            intervals.pop(i)
        else:
            i += 1


def _replace_with(old_text, new_strings, intervals):
    assert len(new_strings) == len(intervals)

    indices = _get_split_indices(intervals)
    assert len(indices) == 2 * len(intervals)

    text_split_by_indices = _split_by_indices(old_text, indices)
    text_without_old_strings = text_split_by_indices[::2]
    assert len(text_without_old_strings) == len(new_strings) + 1

    new_strings.append('')  # to make zip even

    result = _interleave(text_without_old_strings, new_strings)
    return ''.join(result)


def _get_split_indices(intervals):
    indices = [start for (start, _) in intervals] + [end for (_, end) in intervals]
    return list(sorted(indices))


def _split_by_indices(item, indices):
    return [item[i:j] for i, j in zip([0] + indices, indices + [None])]


def _interleave(list1, list2):
    assert len(list1) == len(list2)
    return [x for pair in zip(list1, list2) for x in pair]
