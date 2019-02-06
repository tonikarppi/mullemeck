import os
from dotenv import load_dotenv

load_dotenv()

github_secret = os.getenv('GITHUB_SECRET', default=None)
github_url = os.getenv('GITHUB_URL', default=None)
db_uri = os.getenv('DB_URI', default=None)


def assert_not_none(variable, error_message):
    assert variable is not None, error_message


def validate_environment_variables():
    assert_not_none(
        github_secret, 'GITHUB_SECRET environment variable required.')

    assert_not_none(
        github_url, 'GITHUB_URL environment variable required.')

    assert_not_none(
        db_uri, 'DB_URI environment variable required.')
