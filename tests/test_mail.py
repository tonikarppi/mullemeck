from mullemeck import email
from flask_mail import Mail

app = email.app
app.config['MAIL_DEFAULT_SENDER'] = "mulle@meck.net"
app.config['MAIL_PORT'] = 1025
app.config['MAIL_SERVER'] = "localhost"
email.mail = Mail(app)


def test_send_mail():
    app.config["TESTING"] = True
    email.mail = Mail(app)

    subject = "test"
    content = "<p> hi </p>"
    recipient = "bob@alicemail.net"
    with email.mail.record_messages() as outbox:
        email.send_mail(subject, content, recipient)
    assert len(outbox) == 1
    assert outbox[0].subject == subject
    assert content in outbox[0].html
    assert outbox[0].recipients == [recipient]


def test_smtp_server_integration():
    pass
