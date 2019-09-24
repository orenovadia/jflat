from __future__ import unicode_literals

from contextlib import contextmanager


def flatten_json_object(obj):
    # type: (dict) -> dict
    return Flattener().flatten(obj)


class Flattener(object):
    def __init__(self) -> None:
        self._tracker = PathTracker()
        self._result = {}

    def flatten(self, obj):
        if not isinstance(obj, dict):
            raise TypeError('Root must be a obj, got {}'.format(type(obj)))
        self._visit(obj)
        return self._result

    def _visit(self, obj):
        if isinstance(obj, dict):
            self._visit_dict(obj)
        else:
            self._visit_value(obj)

    def _visit_dict(self, obj):
        for key, value in obj.items():
            with self._tracker.inside(key):
                self._visit(value)

    def _visit_value(self, value):
        self._result[self._tracker.path()] = value


class CanNotBeFlattenedError(ValueError):
    pass


class PathTracker(object):
    def __init__(self) -> None:
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
        # However, it is more elegant than keeping all the prefixes at all times
        # And might even be faster for workloads with unbalanced nesting
        return '.'.join(self._stack)
