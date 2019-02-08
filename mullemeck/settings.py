import os
from dotenv import load_dotenv

load_dotenv()

github_secret = os.getenv('GITHUB_SECRET', default=None)
github_url = os.getenv('GITHUB_URL', default=None)
db_uri = os.getenv('DB_URI', default=None)
clone_dir = os.getenv("MULLE_CLONE_DIR", default="/tmp/mullemeck/")
db_uri = db_uri if db_uri else 'sqlite:///dev.db'


def assert_truthy(value, error_message):
    assert value, error_message


def validate_environment_variables():

    assert os.access(os.path.dirname(clone_dir), os.W_OK), \
        "Application does not have acess to that path"

    assert_truthy(
        github_secret, 'GITHUB_SECRET environment variable required.')

    assert_truthy(
        github_url, 'GITHUB_URL environment variable required.')
