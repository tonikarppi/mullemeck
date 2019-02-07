from flask_mail import Mail, Message


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
