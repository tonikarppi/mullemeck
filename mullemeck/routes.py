from flask import Flask, request, abort, render_template
from .utils import compute_signature
from .db import Session, Build
from .settings import github_secret, github_url


app = Flask(__name__)


@app.route('/')
def index():
    session = Session()
    builds = session.query(Build).all()
    print(builds)
    return render_template('index.html')


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


@app.teardown_appcontext
def remove_session(error):
    # The session is removed after each request.
    Session.remove()


__all__ = ['app']
