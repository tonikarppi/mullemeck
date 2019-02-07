from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MAIL_DEFAULT_SENDER'] = "mulle@meck.net"
app.config['MAIL_PORT'] = 1025
app.config['MAIL_SERVER'] = "localhost"
mail = Mail(app)


def send_mail(subject, html_content, recipient):
    with app.app_context():
        message = Message(subject=subject, recipients=[
                          recipient], html=html_content)
        mail.send(message)
