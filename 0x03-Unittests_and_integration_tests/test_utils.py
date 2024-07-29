#!/usr/bin/env python3
"""This module implements unit testing"""
import unittest
from parameterized import parameterized
from unittest.mock import Mock, patch
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


class TestGetJson(unittest.TestCase):
    """
    Test case for the get_json function in the utils module.

    This class uses the unittest framework to test the behavior of the
    get_json function, ensuring it handles different URLs and returns
    the expected JSON payloads without making actual HTTP requests.
    """

    @parameterized.expand([
        ('http://example.com', {'payload': True}),
        ('http://holberton.io', {'payload': False})
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        Test that utils.get_json returns the expected result for various URLs.

        This test method patches requests.get to return a mock response
        with a custom json method. It verifies that get_json correctly
        retrieves the JSON data for different test URLs and payloads,
        ensuring the mocked get method is called once per URL.

        Parameters
        ----------
        test_url : str
            The URL to be tested.
        test_payload : dict
            The expected JSON payload.
        mock_get : unittest.mock.Mock
            The patched requests.get method.

        Test Cases
        ----------
        - test_url="http://example.com", test_payload={"payload": True}
        - test_url="http://holberton.io", test_payload={"payload": False}

        Asserts
        -------
        - The mocked get method is called exactly once per input URL.
        - The output of get_json is equal to the expected test_payload.
        """
        mock_response = Mock()
        # Set the mock response to return the test payload
        mock_response.json.return_value = test_payload
        # Assign the mock response to the mock get method
        mock_get.return_value = mock_response

        # Call the function under test
        result = utils.get_json(test_url)

        # Check that the mock get method was called with the correct URL
        mock_get.assert_called_once_with(test_url)
        # Check that the result matches the expected payload
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    Tests the memoize decorator to ensure it caches method results.
    """

    def test_memoize(self):
        """
        Verifies that a_method is called only once when a_property is
        accessed multiple times.
        """
        class TestClass:

            def a_method(self):
                return 42

            @utils.memoize
            def a_property(self):
                return self.a_method()

        test_instance = TestClass()

        with patch.object(test_instance, 'a_method',
                          return_value=42) as mock_method:
            # Call a_property twice
            result1 = test_instance.a_property
            result2 = test_instance.a_property

            # Check the results are correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Assert a_method was only called once
            mock_method.assert_called_once()
