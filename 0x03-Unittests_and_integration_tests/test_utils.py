#!/usr/bin/env python3
"""This module implements unit testing"""
import unittest
from parameterized import parameterized
import utils


class TestAccessNestedMap(unittest.TestCase):
    """
    Test case for the access_nested_map function in the utils module.

    This class contains unit tests that verify the behavior of the
    access_nested_map function with different nested map inputs and key paths.
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {'b': 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
        ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Tests the access_nested_map function with various nested map inputs and
        key paths.

        Parameters
        ----------
        nested_map : dict
            The nested map to access.
        path : tuple
            The sequence of keys representing the path to the value.
        expected : any
            The expected value to be returned by access_nested_map.

        Asserts
        -------
        The function asserts that the returned value from access_nested_map
        matches the expected value for each test case.
        """
        self.assertEqual(utils.access_nested_map(nested_map, path), expected)

    @parameterized.expand([
            ({}, ("a",), KeyError),
            ({"a": 1}, ("a", "b"), KeyError)
            ])
    def test_access_nested_map_exception(self, nested_map, path, expected):
        """
        Tests the access_nested_map function for exceptions.

        This test method verifies that the access_nested_map function raises
        the expected exceptions for invalid paths in the nested map.

        Parameters
        ----------
        nested_map : dict
            The nested map to access.
        path : tuple
            The sequence of keys representing the path to the value.
        expected : Exception
            The expected exception to be raised by access_nested_map.

        Asserts
        -------
        The function asserts that the expected exception is raised when
        accessing an invalid path in the nested map.
        """
        with self.assertRaises(expected):
            utils.access_nested_map(nested_map, path)
