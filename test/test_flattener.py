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
            self._flatten(None)

    def test_all_types_of_leaf_values_are_legitimate(self):
        values = [1, 1.2, None, float('inf'), 'str']
        for value in values:
            self._assert_flatten({'a': {'b': value}}, {'a.b': value})

    def test_arrays_are_not_supported(self):
        with self.assertRaises(CanNotBeFlattenedError) as raises_context:
            self._flatten({'a': {'b': []}})
        error_message = repr(raises_context.exception)
        self.assertIn('At a.b', error_message)
        self.assertIn('Arrays can not be flattened', error_message)

    def test_unexpected_json_values(self):
        with self.assertRaises(Exception) as raises_context:
            self._flatten({'c': 4j})
        self.assertIn('Unexpected', repr(raises_context.exception))

    def _assert_flatten(self, nested, expected):
        actual = self._flatten(nested)
        self.assertDictEqual(expected, actual)

    def test_several_leaf_values(self):
        nested = {
            "a": 1,
            "b": True,
            "c": {
                "d": 3,
                "e": "test"
            }
        }
        expected = {
            "a": 1,
            "b": True,
            "c.d": 3,
            "c.e": "test"
        }
        self._assert_flatten(nested, expected)

    def _flatten(self, obj):
        return flatten_json_object(obj)
