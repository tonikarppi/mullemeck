"""
This module contains functions that should tie together the modules
in the package.
"""

from mullemeck.routes import app, queue
from mullemeck.db import create_tables
from mullemeck.settings import validate_environment_variables, db_uri
from mullemeck.utils import add_samples_to_db


def run(app, *args, **kwargs):
    """
    Starts the `app` together with the task queue. When the app exits,
    the task queue is guaranteed to terminate.
    """
    try:
        queue.start()
        app.run(*args, **kwargs)
    finally:
        queue.stop()


def main(*args):
    """
    Runs the appropriate functionality depending on the input argument.

    The possible options are:
    - create_tables -- Creates the tables required by the app.
    - add_samples -- Adds sample entries to the database.
    - develop -- Starts the app in development mode.
    - production -- Starts the app in production mode.

    This function throws an `AssertionError` if the required environment
    variables are not supplied.
    """
    validate_environment_variables()
    assert len(args) == 1, \
        'Expected 1 argument <create_tables|add_samples|develop|production>'
    arg = args[0]
    if arg == 'create_tables':
        print(f'Creating tables in: {db_uri}')
        create_tables()
    elif arg == 'add_samples':
        print(f'Adding sample entries to: {db_uri}')
        add_samples_to_db()
    elif arg == 'develop':
        run(app, debug=True)
    elif arg == 'production':
        run(app, host="0.0.0.0")
    else:
        raise ValueError(f'Unexpected argument: {arg}')


__all__ = ['main']
