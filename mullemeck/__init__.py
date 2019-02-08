from mullemeck.routes import app, queue
from mullemeck.db import create_tables
from mullemeck.settings import validate_environment_variables, db_uri
from mullemeck.utils import add_samples_to_db


def main(*args):
    validate_environment_variables()
    assert len(args) == 1, 'Expected 1 argument <setup|develop|production>'
    arg = args[0]
    if arg == 'create_tables':
        print(f'Creating tables in: {db_uri}')
        create_tables()
    elif arg == 'add_samples':
        print(f'Adding sample entries to: {db_uri}')
        add_samples_to_db()
    elif arg == 'develop':
        queue.start()
        app.run(debug=True)
        queue.stop()
    elif arg == 'production':
        queue.start()
        app.run(host="0.0.0.0")
        queue.stop()
    else:
        raise ValueError(f'Unexpected argument: {arg}')


__all__ = ['app']
