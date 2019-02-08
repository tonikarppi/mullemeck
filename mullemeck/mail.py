from flask import render_template
from flask_mail import Mail, Message
from mullemeck import settings
from mullemeck.db import Build, Session


def send_mail(app, subject, html_content, recipient):
    """
    This function sends an email to the email addresses in recipient.
    It configures the mail parameters for Flask app.
    """
    app.config['MAIL_DEFAULT_SENDER'] = "mulle@meck.net"
    app.config['MAIL_PORT'] = 1025
    app.config['MAIL_SERVER'] = "localhost"
    mail = Mail(app)

    with app.app_context():
        message = Message(subject=subject, recipients=[
                          recipient], html=html_content)
        mail.send(message)


def notify_build(app, commit_id):
    session = Session()
    build = session.query(Build) \
        .filter(commit_id=commit_id) \
        .first()
    content = render_template("build_email.html",
                              url=settings.website_url
                              + "/commit-view/"+commit_id,
                              **build)

    send_mail(app, "Build notification", content, settings.notifictaion_email)
