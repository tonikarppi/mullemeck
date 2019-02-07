from flask import Flask, request, abort, render_template
from .utils import compute_signature
from .db import Session, Build
from flask_sqlalchemy import SQLAlchemy
from .settings import github_secret, github_url
from .build import run_build
# from .email import send_mail
from .processing import TaskQueue
import subprocess


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../dev.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class BuildValues(db.Model):
    __tablename__ = 'build'
    id = db.Column(db.Integer, primary_key=True)
    commit_id = db.Column(db.String, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(
        db.Enum('processing', 'failed', 'success'), nullable=False)
    log_message = db.Column(db.UnicodeText, default='')


def process_commit(commit_id, repository_url):
    # Runs the build.
    build_status, directory = run_build(repository_url, commit_id)
    # Removes the temporary directory
    subprocess.call('rm -rf ' + directory, shell=True)

    # Sends an email notification with the result of the build.
    # email_adresses = 'karppitoni@gmail.com, lars.cg.lundin@gmail.com, ' + \
    #     'alxyshubt@gmail.com, isakp@kth.se, albladh@kth.se'
    # subject = 'Build for ' + commit_id + ' was ' + build_status
    # html_content = "<h1> Build for " + commit_id + \
    #     "</h1><br/><h3>" + build_status + "</h3>"

    # send_mail(subject, email_adresses, html_content)


queue = TaskQueue(process_commit)


@app.route('/build_list/<int:page_num>')
def build_list(page_num):
    build_list = BuildValues.query.paginate(
        per_page=5, error_out=True, page=page_num)
    return render_template('build_list.html', build_list=build_list)


@app.route('/build_view/<int:page_num>')
def build_view(page_num):
    build_list = BuildValues.query.paginate(
        per_page=1, error_out=True, page=page_num)
    return render_template('build_view.html', build_list=build_list)


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

    queue.push(commit_id=commit_id, repository_url=repository_url)

    return '', 200


@app.teardown_appcontext
def remove_session(error):
    # The session is removed after each request.
    Session.remove()


__all__ = ['app', 'queue']
