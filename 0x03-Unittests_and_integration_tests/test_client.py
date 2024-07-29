#!/usr/bin/env python3
"""This module implements unit testing"""
import unittest
from client import GithubOrgClient
import utils
from unittest.mock import Mock, patch, PropertyMock
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

    def test_public_repos_url(self):
        with patch("client.GithubOrgClient.org",
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/google/repo"}

            client = GithubOrgClient("repos_url")
            result = client._public_repos_url

            self.assertEqual(result, "https://api.github.com/orgs/google/repo")
            mock_org.assert_called_once()
