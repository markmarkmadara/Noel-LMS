from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "bcplms.qc@gmail.com"
app.config["MAIL_PASSWORD"] = "gpyxnpypngilmhef"
app.config["MAIL_DEFAULT_SENDER"] = "bcplms.qc@gmail.com"
app.config["MAIL_DEBUG"] = True  # Enable debugging

mail = Mail(app)


@app.route("/")
def send_email():
    try:
        msg = Message("Test Email", recipients=["markmarkmadara@gmail.com"])
        msg.body = "This is a test email."
        mail.send(msg)
        return "Email sent successfully"
    except Exception as e:
        return f"An error occurred: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True)
