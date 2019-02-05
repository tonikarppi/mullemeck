from mullemeck import app
from dotenv import load_dotenv
import os


def validate_environment_variables():
    github_secret = os.getenv('GITHUB_SECRET', default=None)
    github_error_msg = 'GITHUB_SECRET environment variable required.'
    assert github_secret is not None, github_error_msg


def main(args):
    load_dotenv()
    validate_environment_variables()
    debug = 'debug' in args
    app.run(debug=debug)


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
