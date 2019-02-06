from mullemeck.backend import email

app = email.app
app.config["TESTING"] = True
mail = email.mail


def test_send_mail():

    subject = "test"
    content = "<p> hi </p>"
    recipient = "bob@alicemail.net"
    with mail.record_messages() as outbox:
        email.send_mail(subject, content, recipient)
    assert len(outbox) == 1
    assert outbox[0].subject == subject
    assert content in outbox[0].content
    assert outbox[0].recipient == recipient
