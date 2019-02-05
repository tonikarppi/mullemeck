from flask import Flask, request, abort
import os
from .utils import compute_signature


app = Flask(__name__)
github_secret = os.environ.get('GITHUB_SECRET', None)
github_url = os.environ.get('GITHUB_URL', None)


@app.route('/')
def index():
    return '<h1>Hello world!</h1>'


@app.route('/webhook', methods=['POST'])
def webhooks():
    # Only allow authenticated requests.
    if github_secret is None:
        abort(500)

    # Prevents too big requests.
    if request.content_length > 1000 * 1000:
        abort(400)

    # Makes sure the client enabled signature verification.
    github_signature = request.headers.get('X-Hub-Signature', default=None)
    if github_signature is None:
        abort(403)

    # Computes the signature and makes sure they match.
    data = request.get_data()
    computed_signature = compute_signature(github_secret, data)
    if github_signature != computed_signature:
        abort(403)

    req_json = request.get_json()

    # Checks that the request comes from the correct repository.
    repository_url = req_json['repository']['html_url']
    if github_url != repository_url:
        abort(403)

    commit_id = req_json['head_commit']['id']
    print(commit_id)

    # TODO: Start a build based on commit_id.

    return '', 200


__all__ = ['app']
