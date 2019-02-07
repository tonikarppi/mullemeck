from mullemeck import email
from mullemeck.routes import app
from flask_mail import Mail


def test_send_mail():
    app.config["TESTING"] = True
    mail = Mail(app)

    subject = "test"
    content = "<p> hi </p>"
    recipient = "bob@alicemail.net"
    with mail.record_messages() as outbox:
        email.send_mail(app, subject, content, recipient)
    assert len(outbox) == 1
    assert outbox[0].subject == subject
    assert content in outbox[0].html
    assert outbox[0].recipients == [recipient]


def test_smtp_server_integration():
    pass
