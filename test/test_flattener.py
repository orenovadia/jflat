from unittest import TestCase

from jflat import flatten_json_object


class FlattenerTests(TestCase):
    def test_degenerate_case(self):
        self._assert_flatten({}, {})
        self._assert_flatten({'a': 1}, {'a': 1})

    def _assert_flatten(self, nested, expected):
        actual = flatten_json_object(nested)
        self.assertDictEqual(expected, actual)
