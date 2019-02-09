"""
This module contains tests that deal with the database and the ORM.
"""

import pytest
from mullemeck.db import Build, Base
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
from datetime import datetime
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite://')
Session = sessionmaker()


@pytest.fixture(scope='module')
def connection():
    """
    Creates a fixture for a database connection. This connection is kept
    open for the lifetime of all the tests in this module. After the tests
    have finished executing, the connection will automatically close.
    """
    Base.metadata.create_all(engine)
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(scope='function')
def session(connection):
    """
    Creates a fixture for a database session. Each test function will receive
    their own session object. After a test has finished, the changes made by
    the session will be rolled back to its starting state.
    """
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()


@pytest.mark.parametrize('build_args', [
    {
        'commit_id': '4f29b9113316bfe4d090feae8c4e34f131a90728',
        'start_date': datetime(2018, 9, 12),
        'status': 'processing',
        'log_message': 'This part contains log messages from build scripts'
    },
    {
        'commit_id': 'd29c2b9c96f7c33e7c3048aee98fdacfe520803c',
        'start_date': datetime(2019, 1, 14),
        'status': 'failed',
        'log_message': 'This part contains log messages from build scripts'
    },
    {
        'commit_id': '746362310702964e1431d14202dd65165fc9d330',
        'start_date': datetime(2019, 2, 16),
        'status': 'success',
        'log_message': 'This part contains log messages from build scripts'
    }]
)
def test_build_model_success(session, build_args):
    """
    Tests that the `Build` model correctly takes in the required information,
    and persists it in the database.
    """
    build = Build(**build_args)
    session.add(build)
    assert session.query(Build).count() == 1
    entry = session.query(Build).one()
    assert entry.commit_id == build_args['commit_id']
    assert entry.start_date == build_args['start_date']
    assert entry.status == build_args['status']
    assert entry.log_message == build_args['log_message']


@pytest.mark.parametrize('build_args', [
    {
        # No commit_id
        'start_date': datetime(2018, 9, 12),
        'status': 'processing',
        'log_message': 'This part contains log messages from build scripts'
    },
    {
        # No start_date
        'commit_id': 'd29c2b9c96f7c33e7c3048aee98fdacfe520803c',
        'status': 'failed',
        'log_message': 'This part contains log messages from build scripts'
    },
    {
        # No status
        'commit_id': '746362310702964e1431d14202dd65165fc9d330',
        'start_date': datetime(2019, 2, 16),
        'log_message': 'This part contains log messages from build scripts'
    },
    {
        # Invalid status
        'commit_id': '746362310702964e1431d14202dd65165fc9d330',
        'start_date': datetime(2019, 2, 16),
        'log_message': 'This part contains log messages from build scripts',
        'status': 'fake'
    }])
def test_build_model_failure(session, build_args):
    """
    Tests for expected exceptional behavior of the `Build` model, if the
    contract for the accepted values is broken.
    """
    build = Build(**build_args)
    session.add(build)
    with pytest.raises(IntegrityError):
        session.commit()
