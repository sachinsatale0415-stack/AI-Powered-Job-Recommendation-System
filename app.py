import streamlit as st
import tempfile
import base64
import re

from app.resume.parser import extract_text_from_pdf
from app.jobs.fetcher import fetch_jobs
from app.matching.matcher import calculate_match
from app.notifications.email import send_email, notify_admin


# 🔥 PAGE CONFIG
st.set_page_config(page_title="JobBuddy AI", layout="wide")


# 🔥 CLEAN HTML FUNCTION
def clean_html(text):
    if not text:
        return ""
    return re.sub('<.*?>', '', text)


# 🔥 BACKGROUND IMAGE
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg_image = get_base64("assets/bg.png")


# 🔥 CSS
st.markdown(f"""
<style>
.stApp {{
    background-image: url("data:image/png;base64,{bg_image}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.title {{
    text-align: center;
    color: black;
    font-size: 42px;
    font-weight: bold;
}}

.subtitle {{
    text-align: center;
    color: #444;
    font-size: 18px;
    margin-top: -10px;
    margin-bottom: 20px;
}}

.section {{
    background: rgba(0,0,0,0.6);
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 20px;
}}
</style>
""", unsafe_allow_html=True)


# 🔥 HEADER
st.markdown('<div class="title">🚀 JobBuddy AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Find the best jobs tailored to your resume using AI</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


# 🔹 INPUT SECTION
st.markdown('<div class="section">', unsafe_allow_html=True)

# ✅ NEW NAME FIELD (ADDED)
name = st.text_input("👤 Full Name", placeholder="Enter your full name")

uploaded_file = st.file_uploader("📤 Upload Resume", type=["pdf"])
job_title = st.text_input("💼 Job Title", placeholder="Data Analyst")
email = st.text_input("📧 Email", placeholder="your@email.com")

# ✅ PRIVACY LINE (ADDED)
st.caption("⚠️ Your data may be used for analytics and improvement purposes.")

st.markdown('</div>', unsafe_allow_html=True)


# 🔍 BUTTON
if st.button("🔍 Find Jobs"):

    # ✅ UPDATED VALIDATION
    if not uploaded_file or not email or not name:
        st.warning("Please fill all fields (Name, Resume, Email)")

    else:
        # 🔥 SEND ADMIN EMAIL (ADDED)
        notify_admin(name, email, job_title, uploaded_file)

        with st.spinner("🤖 AI is analyzing your resume..."):

            # 🔥 FIX FILE POINTER (IMPORTANT)
            uploaded_file.seek(0)

            # SAVE FILE
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                file_path = tmp.name

            # EXTRACT TEXT
            resume_text = extract_text_from_pdf(file_path).lower()

            if not job_title:
                job_title = "software developer"

            # FETCH JOBS
            jobs = fetch_jobs(job_title)

            matched_jobs = []

            for job in jobs:
                description = clean_html(job.get("description", "").lower())

                score = calculate_match(resume_text, description)

                # FILTER EXPERIENCE
                is_fresher = any(x in description for x in [
                    "fresher", "0-1", "entry level", "junior", "intern"
                ])

                is_senior = any(x in description for x in [
                    "3+ years", "5+ years", "7+ years",
                    "senior", "lead", "manager"
                ])

                if is_senior and not is_fresher:
                    continue

                # BOOST
                if is_fresher:
                    score += 15

                if job_title.lower() in job["title"].lower():
                    score += 10

                # SKIP BAD LINKS
                if not job.get("link") or job["link"] == "#":
                    continue

                matched_jobs.append({
                    "title": clean_html(job["title"]),
                    "company": clean_html(job["company"]),
                    "score": score,
                    "link": job["link"]
                })

            # SORT
            matched_jobs = sorted(
                matched_jobs,
                key=lambda x: x["score"],
                reverse=True
            )

            top_jobs = matched_jobs[:10]

        # 🎯 RESULTS
        st.markdown("## 🎯 Top Results")

        if not top_jobs:
            st.error("No jobs found 😢")

        else:
            for job in top_jobs:

                if job["score"] >= 70:
                    label = "🔥 High Match"
                elif job["score"] >= 50:
                    label = "⭐ Good Match"
                else:
                    label = "⚠️ Low Match"

                with st.container():
                    st.markdown(f"### {job['title']}")
                    st.caption(job["company"])
                    st.success(f"{label} • Match Score: {job['score']:.2f}%")

                    st.link_button("🚀 Apply Now", job["link"])
                    st.markdown("---")

            # 📩 USER EMAIL
            send_email(top_jobs, receiver=email)

            st.success("📩 Jobs sent to your email!")