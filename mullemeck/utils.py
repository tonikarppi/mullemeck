import hmac
import hashlib


def compute_signature(secret, data):
    secret_bytes = bytes(secret, 'utf-8')
    return 'sha1=' + hmac.new(secret_bytes, data, hashlib.sha1).hexdigest()
