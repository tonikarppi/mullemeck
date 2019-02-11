from flask import render_template
from flask_mail import Mail, Message
from mullemeck import settings
from mullemeck.db import Session, Build


def send_mail(app, subject, html_content, recipient):
    """
    This function sends an email to the email addresses in recipient.
    It configures the mail parameters for Flask app.
    """
    app.config['MAIL_DEFAULT_SENDER'] = settings.sender_email
    app.config['MAIL_PORT'] = settings.smtp_port
    app.config['MAIL_SERVER'] = settings.smtp_server
    app.config['MAIL_USERNAME'] = settings.smtp_user
    app.config['MAIL_PASSWORD'] = settings.smtp_password
    app.config['MAIL_SSL'] = settings.smtp_tls
    app.config['MAIL_TLS'] = settings.smtp_ssl

    mail = Mail(app)

    with app.app_context():
        message = Message(subject=subject, recipients=[
                          recipient], html=html_content)
        mail.send(message)


def notify_build(app, commit_id, committer_email):
    session = Session()
    build = session.query(Build) \
        .filter(Build.commit_id == commit_id) \
        .first()
    content = render_template("build_email.html",
                              url=settings.website_url
                              + "/commit-view/"+commit_id,
                              **build.__dict__)

    send_mail(app, "Build notification", content, committer_email)
