import smtplib
from email.mime.text import MIMEText


def send_email(job_list, receiver):
    sender_email = "projectgroup5.vita@gmail.com"
    password = "puvvdogcvcjcdfzy"

    subject = f"🚀 Top {len(job_list)} AI-Matched Jobs"

    body = "Here are your matched jobs:\n\n"

    for i, job in enumerate(job_list, 1):
        body += f"""
{i}. {job['title']} at {job['company']}
Match: {job['score']:.2f}%
Apply: {job['link']}
--------------------------
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver, msg.as_string())
    server.quit()