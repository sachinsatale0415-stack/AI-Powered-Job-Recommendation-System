import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


# 📩 SEND JOBS TO USER (STRUCTURED FORMAT)
def send_email(jobs, receiver):

    sender = st.secrets["EMAIL_ADDRESS"]
    password = st.secrets["EMAIL_PASSWORD"]

    subject = "🚀 Your JobBuddy AI Results"

    # ✅ CLEAN STRUCTURED BODY
    body = "Here are your matched jobs:\n\n"

    for i, job in enumerate(jobs, start=1):
        body += (
            f"{i}. {job['title']} at {job['company']}\n"
            f"Match: {job['score']:.2f}%\n"
            f"Apply: {job['link']}\n"
            f"{'-'*30}\n\n"
        )

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


# 🚀 SEND USER DETAILS TO ADMIN (WITH RESUME)
def notify_admin(user_name, user_email, job_title, resume_file):

    sender = st.secrets["EMAIL_ADDRESS"]
    password = st.secrets["EMAIL_PASSWORD"]
    receiver = st.secrets["ADMIN_EMAIL"]

    subject = "🚀 New JobBuddy User"

    # ✅ ADMIN EMAIL BODY
    body = f"""
🚀 New User Activity - JobBuddy AI

👤 Name: {user_name}
📧 Email: {user_email}
💼 Job Title: {job_title}
"""

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    msg.attach(MIMEText(body, "plain"))

    # 📄 ATTACH RESUME FILE
    try:
        if resume_file:
            resume_file.seek(0)  # IMPORTANT

            file_data = resume_file.read()

            part = MIMEApplication(file_data, Name="resume.pdf")
            part['Content-Disposition'] = 'attachment; filename="resume.pdf"'

            msg.attach(part)
    except Exception as e:
        print("Attachment error:", e)

    # 📤 SEND EMAIL
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
    except Exception as e:
        print("Admin email error:", e)