"""
This module deals with the database related functionality.

The components from the module that clients will probably use
the most are the `Build` model and the `Session` registry object.
"""

from mullemeck.settings import db_uri
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, DateTime, Enum, UnicodeText, String

Base = declarative_base()


class Build(Base):
    """
    This model represents a repository build for a particular commit.
    """

    __tablename__ = 'build'

    id = Column(Integer, primary_key=True)
    commit_id = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    status = Column(Enum('processing', 'failed', 'success'), nullable=False)
    log_message = Column(UnicodeText, default='')

    def __repr__(self):
        return f'Build({self.commit_id})'


# Sets up the engine which manages DB connections.
engine = create_engine(db_uri)

# Creates the session manager which is used for interacting with DB.
Session = scoped_session(sessionmaker(bind=engine))


def create_tables():
    """
    Creates the tables on the database, which are representations
    for the model objects defined in this module.
    This function requires that the engine was given a valid database URI.
    """
    Base.metadata.create_all(engine)


__all__ = ['Session', 'Build', 'Base', 'create_tables']
