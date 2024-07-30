#!/usr/bin/env python3
"""This module implements unit testing"""
import unittest
from client import GithubOrgClient
import utils
from unittest.mock import Mock, patch, PropertyMock
from parameterized import parameterized, parameterized_class
import requests
from fixtures import TEST_PAYLOAD


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

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
        ])
    def test_has_license(self, repo, license_key, expected):
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up class method to start patching requests.get"""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Mock the .json() method to return different payloads based on the URL
        def side_effect(url):
            if url == "https://api.github.com/orgs/google":
                return Mock(json=lambda: cls.org_payload)
            elif url == "https://api.github.com/orgs/google/repos":
                return Mock(json=lambda: cls.repos_payload)
            return Mock(json=lambda: None)

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Tear down class method to stop patching"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        client = GithubOrgClient("google")
        repos = client.public_repos("apache-2.0")
        self.assertEqual(repos, self.apache2_repos)
