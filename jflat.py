from __future__ import unicode_literals

import argparse
import json
import sys
from contextlib import contextmanager

try:
    string_type = unicode
except:
    string_type = str


def flatten_json_object(obj):
    # type: (dict) -> dict
    return Flattener().flatten(obj)


class Flattener(object):
    def __init__(self):
        self._tracker = PathTracker()
        self._result = {}

    def flatten(self, obj):
        self._validate(isinstance(obj, dict), 'Root must be a obj, got {}'.format(type(obj)))
        self._visit(obj)
        return self._result

    def _visit(self, obj):
        if isinstance(obj, dict):
            self._visit_dict(obj)

        elif obj is None or isinstance(obj, (bool, int, float, string_type)):
            self._visit_leaf(obj)

        elif isinstance(obj, list):
            self._error('Arrays can not be flattened')

        else:
            raise self._error('Unexpected value in primitive JSON object {}'.format(type(obj)))

    def _visit_dict(self, obj):
        for key, value in obj.items():
            self._validate_key(key)
            with self._tracker.inside(key):
                self._visit(value)

    def _visit_leaf(self, value):
        self._result[self._tracker.path()] = value

    def _validate_key(self, key):
        self._validate(isinstance(key, string_type), 'Object keys must be strings: '
                                             'got {} of type {}'.format(key, type(key)))
        self._validate('.' not in key, 'Object keys may not contain ".": {}'.format(key))

    def _validate(self, condition, message):
        if not condition:
            self._error(message)

    def _error(self, message):
        # type: (str) -> None
        raise CanNotBeFlattenedError('At {}: {}'.format(self._tracker.path(), message))


class CanNotBeFlattenedError(TypeError):
    pass


class PathTracker(object):
    def __init__(self):
        self._stack = []

    @contextmanager
    def inside(self, key):
        self._stack.append(key)
        try:
            yield
        finally:
            self._stack.pop()

    def path(self):
        # This method is not optimal for balanced trees
        # because we concat the same prefix multiple times
        # However, it is more elegant than keeping a stack of
        # all the prefixes so far
        # And it might even be faster for workloads with unbalanced nesting
        return '.'.join(self._stack)


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    args = parser.parse_args()
    _flatten_file(args.infile)


def _flatten_file(infile):
    nested = json.load(infile, encoding='utf-8')
    flat = flatten_json_object(nested)
    print(json.dumps(flat, indent=2))


if __name__ == '__main__':
    _main()
