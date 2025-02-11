from __future__ import unicode_literals

import json
import subprocess
from unittest import TestCase

import jflat
from jflat import flatten_json_object, CanNotBeFlattenedError


class FlattenerTests(TestCase):
    def test_degenerate_case(self):
        self._assert_flatten({}, {})
        self._assert_flatten({'a': 1}, {'a': 1})

    def test_root_must_be_an_object(self):
        # for instance, `null` is a legitimate json object
        self._assert_error(None, 'Root must be a obj')

    def test_all_types_of_leaf_values_are_legitimate(self):
        values = [1, 1.2, None, float('inf'), 'str']
        for value in values:
            self._assert_flatten({'a': {'b': value}}, {'a.b': value})

    def test_arrays_are_not_supported(self):
        self._assert_error({'a': {'b': []}}, 'Arrays can not be flattened')

    def test_errors_are_reported_with_their_location_in_the_tree(self):
        self._assert_error({'a': {'b': []}}, 'At a.b')

    def test_value_of_unexpected_type(self):
        self._assert_error({'c': 4j}, 'Unexpected')

    def test_several_leaf_values(self):
        nested = {
            "a": 1,
            "b": True,
            "c": {
                "d": 3,
                "e": "test",
                "f": None
            }
        }
        expected = {
            "a": 1,
            "b": True,
            "c.d": 3,
            "c.e": "test",
            "c.f": None
        }
        self._assert_flatten(nested, expected)

    def test_unacceptable_object_keys(self):
        self._assert_error({1: 2})
        self._assert_error({'a.b': 2})

    def test_end_to_end_cli_application(self):
        proc = subprocess.Popen(['python', jflat.__file__], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        input_ = json.dumps({'a': {'b': 1}}).encode('utf8')
        expected = {'a.b': 1}

        stdout, _ = proc.communicate(input_)
        self.assertEqual(expected, json.loads(stdout.decode('utf-8')))

    def _assert_flatten(self, nested, expected):
        actual = self._flatten(nested)
        self.assertDictEqual(expected, actual)

    def _assert_error(self, nested, expected_message_substring=None):
        with self.assertRaises(CanNotBeFlattenedError) as raises_context:
            self._flatten(nested)

        if expected_message_substring:
            self.assertIn(expected_message_substring, repr(raises_context.exception))

    @staticmethod
    def _flatten(obj):
        return flatten_json_object(obj)
