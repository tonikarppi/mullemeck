from flask import Flask, request, abort, render_template
from mullemeck.utils import compute_signature
from mullemeck.db import Session, Build
from mullemeck.settings import github_secret, github_url
from mullemeck.build import run_build
from mullemeck.mail import notify_build
# from .email import send_mail
from mullemeck.processing import TaskQueue
import subprocess
from mullemeck.paginator import Paginator


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../dev.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def process_commit(commit_id, repository_url, committer_email):
    # Runs the build.
    build_status, directory = run_build(repository_url, commit_id)
    # Removes the temporary directory
    subprocess.call('rm -rf ' + directory, shell=True)

    notify_build(app, commit_id, committer_email)


queue = TaskQueue(process_commit)


@app.route('/build_list/<int:page_num>')
def build_list(page_num):
    session = Session()
    build_list = Paginator(session.query(Build).all(), 5, page_num)
    return render_template('build_list.html', build_list=build_list)


@app.route('/build_view/<int:page_num>')
def build_view(page_num):
    session = Session()
    build_list = Paginator(session.query(Build).all(), 1, page_num)
    return render_template('build_view.html', build=build_list.list[0][0])


@app.route('/commit_view/<string:commit>')
def commit_view(commit):
    session = Session()
    build = session.query(Build) \
        .filter(Build.commit_id == commit)\
        .first()
    return render_template('build_view.html', build=build)


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

    commit = req_json['head_commit']
    commit_id = commit['id']
    committer_email = commit['committer']['email']

    queue.push(commit_id=commit_id,
               repository_url=repository_url,
               committer_email=committer_email)

    return '', 200


@app.teardown_appcontext
def remove_session(error):
    # The session is removed after each request.
    Session.remove()


__all__ = ['app', 'queue']
