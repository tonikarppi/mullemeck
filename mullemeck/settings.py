"""
Contains values passed in from the local environment, and helpers that work
with them.
"""

import os
from dotenv import load_dotenv

load_dotenv()

github_secret = os.getenv('GITHUB_SECRET', default=None)
github_url = os.getenv('GITHUB_URL', default=None)
website_url = os.getenv('MULLE_URL', default="localhost")
smtp_server = os.getenv('SMTP_SERVER', default="localhost")
smtp_port = os.getenv('SMTP_PORT', default=25)
smtp_user = os.getenv('SMTP_USER', default=None)
smtp_password = os.getenv('SMTP_PASSWORD', default=None)
smtp_tls = os.getenv('SMTP_TLS', default=False)
smtp_ssl = os.getenv('SMTP_SSL', default=False)
sender_email = os.getenv('MULLE_EMAIL', default="mulle@meck.net")
db_uri = os.getenv('DB_URI', default=None)
clone_dir = os.getenv("MULLE_CLONE_DIR", default="/tmp/mullemeck")
db_uri = db_uri if db_uri else 'sqlite:///dev.db'


def assert_truthy(value, error_message):
    """
    Identical to the regular `assert` statement, but allows for splitting
    across multiple lines because of the parentheses.
    """
    assert value, error_message


def validate_environment_variables():
    """
    Throws an `AssertionError` if any of the required environment variables
    are not correctly provided.
    """

    assert os.access(os.path.dirname(clone_dir), os.W_OK), \
        "Application does not have access to that path"

    assert_truthy(
        github_secret, 'GITHUB_SECRET environment variable required.')

    assert_truthy(
        github_url, 'GITHUB_URL environment variable required.')
