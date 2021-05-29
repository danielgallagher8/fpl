"""
Email notification system for trading app
"""

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

receiver_email = ''
sender_email = ''
password = ''
    
def notif(msg, sender_email=sender_email, receiver_email=receiver_email, subject='Stock Alert', text='text'):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    
    if text == 'text':
        html = """\
        <html>
        <head>
        </head>
        <body>
        {0}
        </body>
        </html>""".format(msg)
    elif text == 'html':
        html = msg
    
    part = MIMEText(html, "html")
    message.attach(part)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
                        sender_email, receiver_email, message.as_string()
        )
