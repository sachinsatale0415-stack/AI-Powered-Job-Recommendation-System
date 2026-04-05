import streamlit as st
import tempfile
import base64
import re

from app.resume.parser import extract_text_from_pdf
from app.jobs.fetcher import fetch_jobs
from app.matching.matcher import calculate_match
from app.notifications.email import send_email


# 🔥 PAGE CONFIG
st.set_page_config(page_title="JobBuddy AI", layout="wide")


# 🔥 CLEAN HTML
def clean_html(text):
    if not text:
        return ""
    return re.sub('<.*?>', '', text)


# 🔥 LOAD BACKGROUND
def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg = get_base64("assets/bg.png")


# 🔥 GLOBAL CSS (THIS MAKES YOUR UI EXACTLY SAME)
st.markdown(f"""
<style>

/* Background */
.stApp {{
    background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.75)),
                url("data:image/png;base64,{bg}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* Title */
.title {{
    text-align: center;
    color: white;
    font-size: 46px;
    font-weight: 700;
    margin-top: 30px;
}}

.subtitle {{
    text-align: center;
    color: #ddd;
    font-size: 18px;
    margin-bottom: 40px;
}}

/* Glass Card */
.card {{
    width: 50%;
    margin: auto;
    background: rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255,255,255,0.2);
    margin-bottom: 20px;
}}

/* Labels */
.label {{
    color: #ffffff;
    font-size: 16px;
    margin-bottom: 8px;
}}

/* Input Fields */
input {{
    background-color: rgba(255,255,255,0.1) !important;
    color: white !important;
}}

/* Button */
div.stButton > button {{
    background: linear-gradient(90deg, #4F46E5, #7C3AED);
    color: white;
    padding: 14px 40px;
    border-radius: 12px;
    font-size: 18px;
    border: none;
    display: block;
    margin: 20px auto;
}}

div.stButton > button:hover {{
    transform: scale(1.05);
    transition: 0.2s;
}}

</style>
""", unsafe_allow_html=True)


# 🚀 HERO SECTION
st.markdown('<div class="title">🚀 JobBuddy AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Find the best jobs tailored to your resume using AI</div>', unsafe_allow_html=True)


# 📤 Upload Resume
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="label">📤 Upload Resume</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["pdf"])
st.markdown('</div>', unsafe_allow_html=True)


# 💼 Job Title
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="label">💼 Job Title</div>', unsafe_allow_html=True)
job_title = st.text_input("", placeholder="e.g. Data Analyst")
st.markdown('</div>', unsafe_allow_html=True)


# 📧 Email
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="label">📧 Email</div>', unsafe_allow_html=True)
email = st.text_input("", placeholder="your@email.com")
st.markdown('</div>', unsafe_allow_html=True)


# 🚀 BUTTON
find = st.button("🚀 Find Jobs")


# 🔍 LOGIC (UNCHANGED)
if find:

    if not uploaded_file or not email:
        st.warning("Please upload resume and enter email")

    else:
        with st.spinner("🤖 AI is analyzing your resume..."):

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                file_path = tmp.name

            resume_text = extract_text_from_pdf(file_path).lower()

            if not job_title:
                job_title = "software developer"

            jobs = fetch_jobs(job_title)

            matched_jobs = []

            for job in jobs:
                description = clean_html(job.get("description", "").lower())

                score = calculate_match(resume_text, description)

                is_fresher = any(x in description for x in [
                    "fresher", "0-1", "entry level", "junior", "intern"
                ])

                is_senior = any(x in description for x in [
                    "3+ years", "5+ years", "7+ years",
                    "senior", "lead", "manager"
                ])

                if is_senior and not is_fresher:
                    continue

                if is_fresher:
                    score += 15

                if job_title.lower() in job["title"].lower():
                    score += 10

                if not job.get("link") or job["link"] == "#":
                    continue

                matched_jobs.append({
                    "title": clean_html(job["title"]),
                    "company": clean_html(job["company"]),
                    "score": score,
                    "link": job["link"]
                })

            matched_jobs = sorted(matched_jobs, key=lambda x: x["score"], reverse=True)
            top_jobs = matched_jobs[:10]

        st.markdown("## 🎯 Top Results")

        if not top_jobs:
            st.error("No jobs found 😢")

        else:
            for job in top_jobs:
                st.markdown(f"### {job['title']}")
                st.caption(job["company"])
                st.success(f"Match Score: {job['score']:.2f}%")
                st.link_button("🚀 Apply Now", job["link"])
                st.markdown("---")

            send_email(top_jobs, receiver=email)
            st.success("📩 Jobs sent to your email!")