# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from undebt.cmd.logger import log
from undebt.pattern.interface import create_find_and_replace
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

            find_and_replace = create_find_and_replace(grammar, replace)
            results = parse_grammar(find_and_replace, text)
            if not results:
                break
            else:
                found.append(len(results))
                text = _transform_results(results, text)

        if found:
            log.info('=> pattern {} found {} time(s) in {} pass(es)'
                     .format(i + 1, sum(found), len(found)))
        else:
            log.info('__ pattern {} not found'
                     .format(i + 1))

    return text


def _transform_results(results, text):
    new_strings = []
    intervals = []

    for replace_result, start, end in results:

        replace_list = replace_result.asList()
        assert len(replace_list) == 1
        replace_item = replace_list[0]

        if replace_item is not None:
            new_strings.append(replace_item)
            intervals.append((start, end))

    return _replace_with(text, new_strings, intervals)


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
