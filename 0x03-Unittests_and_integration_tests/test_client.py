#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class.
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    Test cases for GithubOrgClient methods.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct data."""
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_payload)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct repos_url from org."""
        test_payload = {
            "repos_url": "https://api.github.com/orgs/testorg/repos"
        }

        with patch.object(GithubOrgClient, "org", return_value=test_payload):
            client = GithubOrgClient("testorg")
            result = client._public_repos_url
            self.assertEqual(result, test_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected list and calls get_json once."""
        test_repos = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = test_repos

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=property
        ) as mock_url:
            mock_url.return_value = (
                "https://api.github.com/orgs/testorg/repos"
            )

            client = GithubOrgClient("testorg")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/testorg/repos"
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean based on license key."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


# ------------------------------------------------------------------ #
# Integration test class
# ------------------------------------------------------------------ #

@parameterized_class(                      # type: ignore[misc]
    ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
    TEST_PAYLOAD,
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration-style tests that rely on real fixtures."""

    @classmethod
    def setUpClass(cls):
        """
        Patch requests.get once for the entire parameterized class.

        The first call to requests.get(url).json() must return the org
        payload; the second call must return the repos payload.
        """
        cls.get_patcher = patch('requests.get')
        mocked_get = cls.get_patcher.start()

        def side_effect(url):
            if "orgs" in url:
                return Mock(**{'json.return_value': cls.org_payload})
            if "repos" in url:
                return Mock(**{'json.return_value': cls.repos_payload})
            return Mock(**{'json.return_value': {}})

        mocked_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop requests.get patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """public_repos returns full repo list from fixtures."""
        client = GithubOrgClient("anyorg")  # name irrelevant – mocked
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """public_repos filters by license key (apache-2.0)."""
        client = GithubOrgClient("anyorg")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
