import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


# 📩 SEND JOBS TO USER
def send_email(jobs, receiver):
    sender = st.secrets["EMAIL_ADDRESS"]
    password = st.secrets["EMAIL_PASSWORD"]

    subject = "🚀 Your JobBuddy AI Results"

    body = "Here are your top job matches:\n\n"

    for job in jobs:
        body += f"{job['title']} - {job['company']}\nApply: {job['link']}\n\n"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
    except Exception as e:
        print("User email error:", e)


# 🚀 SEND USER DETAILS TO ADMIN
def notify_admin(user_name, user_email, job_title, resume_file):

    sender = st.secrets["EMAIL_ADDRESS"]
    password = st.secrets["EMAIL_PASSWORD"]
    receiver = st.secrets["ADMIN_EMAIL"]

    body = f"""
🚀 New User Activity - JobBuddy AI

👤 Name: {user_name}
📧 Email: {user_email}
💼 Job Title: {job_title}
"""

    msg = MIMEMultipart()
    msg["Subject"] = "🚀 New JobBuddy User"
    msg["From"] = sender
    msg["To"] = receiver

    msg.attach(MIMEText(body, "plain"))

    # 📄 Attach Resume
    if resume_file:
        file_data = resume_file.read()
        part = MIMEApplication(file_data, Name="resume.pdf")
        part['Content-Disposition'] = 'attachment; filename="resume.pdf"'
        msg.attach(part)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
    except Exception as e:
        print("Admin email error:", e)