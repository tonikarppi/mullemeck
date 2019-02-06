from mullemeck.routes import app
from .db import create_tables
from .settings import validate_environment_variables


def main(*args):
    validate_environment_variables()
    assert len(args) == 1, 'Expected 1 argument <setup|develop|production>'
    arg = args[0]
    if arg == 'setup':
        create_tables()
    elif arg == 'develop':
        app.run(debug=True)
    elif arg == 'production':
        app.run()
    else:
        raise ValueError(f'Unexpected argument: {arg}')


__all__ = ['app']
