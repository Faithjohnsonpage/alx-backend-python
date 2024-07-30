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

    @patch('utils.requests.get')
    def test_public_repos(self, mock_get):
        # Define the payload to return from the mocked requests.get
        payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": {"key": "gpl-3.0"}},
        ]

        # Create a mock response object
        mock_response = Mock()
        mock_response.json.return_value = payload
        mock_get.return_value = mock_response

        # Mock _public_repos_url to return a specific URL
        with patch.object(GithubOrgClient, '_public_repos_url',
                          new_callable=PropertyMock) as mock_repos_url:
            mock_repos_url.return_value = \
                    "https://api.github.com/orgs/google/repos"

            client = GithubOrgClient("google")
            result = client.public_repos()

            # Expected result from the payload
            expected_result = ["repo1", "repo2", "repo3"]

            # Assert the result matches the expected result
            self.assertEqual(result, expected_result)

            # Ensure the mocked property and get_json were called once
            mock_repos_url.assert_called_once()
            url = "https://api.github.com/orgs/google/repos"
            mock_get.assert_called_once_with(url)
