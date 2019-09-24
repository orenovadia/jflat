from __future__ import unicode_literals

from unittest import TestCase

from jflat import flatten_json_object, CanNotBeFlattenedError


class FlattenerTests(TestCase):
    def test_degenerate_case(self):
        self._assert_flatten({}, {})
        self._assert_flatten({'a': 1}, {'a': 1})

    def test_root_must_be_an_object(self):
        # for instance `null` is a legitimate json object
        with self.assertRaises(TypeError):
            flatten_json_object(None)

    def test_all_types_of_leaf_values_are_legitimate(self):
        values = [1, 1.2, None, float('inf'), 'str']
        for value in values:
            self._assert_flatten({'a': {'b': value}}, {'a.b': value})

    def _assert_flatten(self, nested, expected):
        actual = flatten_json_object(nested)
        self.assertDictEqual(expected, actual)
