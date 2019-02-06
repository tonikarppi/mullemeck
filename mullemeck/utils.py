import hmac
import hashlib
from .db import Session, Build
from datetime import datetime


def compute_signature(secret, data):
    secret_bytes = bytes(secret, 'utf-8')
    return 'sha1=' + hmac.new(secret_bytes, data, hashlib.sha1).hexdigest()


def add_samples_to_db():
    session = Session()
    session.add_all([
        Build(
            commit_id='4f29b9113316bfe4d090feae8c4e34f131a90728',
            start_date=datetime(2018, 9, 12),
            status='processing',
            log_message='This part contains log messages from build scripts'
        ),
        Build(
            commit_id='d29c2b9c96f7c33e7c3048aee98fdacfe520803c',
            start_date=datetime(2019, 1, 14),
            status='failed',
            log_message='This part contains log messages from build scripts'
        ),
        Build(
            commit_id='746362310702964e1431d14202dd65165fc9d330',
            start_date=datetime(2019, 2, 16),
            status='success',
            log_message='This part contains log messages from build scripts'
        ),
    ])
    session.commit()
    Session.remove()
