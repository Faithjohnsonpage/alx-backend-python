#!/usr/bin/env python3
"""This module implements unit testing"""
import unittest
from client import GithubOrgClient
import utils
from unittest.mock import Mock, patch
from parameterized import parameterized
import requests


class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ("google", "https://api.github.com/orgs/google", {"google": "access"}),
        ("abc", "https://api.github.com/orgs/abc", {"abc": "restricted"})
        ])
    @patch("utils.requests.get")
    def test_org(self, org, url, json_load, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = json_load
        mock_get.return_value = mock_response

        client = GithubOrgClient(org)
        result = client.org

        self.assertEqual(result, json_load)
        mock_get.assert_called_once()
