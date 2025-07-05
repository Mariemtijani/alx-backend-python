#!/usr/bin/env python3
"""
Unit tests for the utils.access_nested_map function.
"""

import unittest
from typing import Mapping, Sequence, Any
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """
    Test cases for the access_nested_map function in utils module.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
        self,
        nested_map: Mapping[str, Any],
        path: Sequence[str],
        expected: Any
    ) -> None:
        """Test that access_nested_map returns expected result."""
        self.assertEqual(access_nested_map(nested_map, path), expected)
