import smtplib
from email.mime.text import MIMEText

# Philosophy line

def send_email(to_address, subject, body, html=False):
    """
    Sends an email with philosophy line appended automatically.
    """
    full_body = body + PHILOSOPHY_LINE

    if html:
        msg = MIMEText(full_body, 'html')
    else:
        msg = MIMEText(full_body)

    msg['Subject'] = subject
    msg['From'] = "reeselimitedllc@gmail.com"
    msg['To'] = to_address

    # Send email via Gmail SMTP
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login("reeselimitedllc@gmail.com", "YOUR_APP_PASSWORD")
        server.send_message(msg)
        print(f"Email sent to {to_address}")
