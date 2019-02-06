from mullemeck.routes import app
from .db import create_tables
from .settings import validate_environment_variables
from .utils import add_samples_to_db


def main(*args):
    validate_environment_variables()
    assert len(args) == 1, 'Expected 1 argument <setup|develop|production>'
    arg = args[0]
    if arg == 'create_tables':
        create_tables()
    if arg == 'add_samples':
        add_samples_to_db()
    elif arg == 'develop':
        app.run(debug=True)
    elif arg == 'production':
        app.run()
    else:
        raise ValueError(f'Unexpected argument: {arg}')


__all__ = ['app']
