from mullemeck import settings
import pytest
import os

"""
    Verifies that settings are verified properly
"""


def test_good_settings():
    settings.clone_dir = os.getcwd()
    settings.github_secret = "Secret"
    settings.github_url = "www.github.com"

    # Should not raise
    settings.validate_environment_variables()


def test_bad_github_paramteters():
    settings.github_secret = None
    with pytest.raises(AssertionError):
        settings.validate_environment_variables()
    settings.github_secret = "Secret2"
    settings.github_url = None
    with pytest.raises(AssertionError):
        settings.validate_environment_variables()
    settings.github_url = "www.github2.com"


def test_bad_directory():
    settings.clone_dir = "abc 123 _ */& ilegal dir"
    with pytest.raises(AssertionError):
        settings.validate_environment_variables()
    settings.clone_dir = os.getcwd()
