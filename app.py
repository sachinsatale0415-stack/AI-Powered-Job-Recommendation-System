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


# 🔥 FINAL CLOUD-PROOF CSS
st.markdown(f"""
<style>

/* REMOVE DEFAULT WHITE */
html, body, [class*="css"] {{
    background: transparent !important;
}}

/* BACKGROUND */
.stApp {{
    background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.75)),
                url("data:image/png;base64,{bg}") !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
}}

/* CENTER CONTAINER */
.main-container {{
    width: 480px;
    margin: auto;
    margin-top: 60px;
}}

/* TITLE */
.title {{
    text-align: center;
    color: white;
    font-size: 42px;
    font-weight: bold;
}}

.subtitle {{
    text-align: center;
    color: #ccc;
    margin-bottom: 30px;
}}

/* GLASS CARD */
.glass {{
    background: rgba(255,255,255,0.08) !important;
    padding: 20px !important;
    border-radius: 15px !important;
    backdrop-filter: blur(15px) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    margin-bottom: 20px !important;
}}

/* LABEL */
.label {{
    color: white !important;
    font-size: 15px !important;
    margin-bottom: 8px !important;
}}

/* INPUTS FIX */
input {{
    background: rgba(255,255,255,0.08) !important;
    color: white !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
}}

.stTextInput > div > div > input {{
    background: rgba(255,255,255,0.08) !important;
    color: white !important;
}}

/* FILE UPLOADER FIX */
.stFileUploader > div {{
    background: rgba(255,255,255,0.05) !important;
    border: 1px dashed rgba(255,255,255,0.3) !important;
    border-radius: 12px !important;
    padding: 15px !important;
}}

.stFileUploader div div {{
    background: transparent !important;
}}

/* BUTTON */
div.stButton > button {{
    background: linear-gradient(90deg, #4F46E5, #7C3AED) !important;
    color: white !important;
    padding: 14px !important;
    border-radius: 12px !important;
    font-size: 18px !important;
    border: none !important;
    width: 100% !important;
}}

div.stButton > button:hover {{
    transform: scale(1.05);
    transition: 0.2s;
}}

</style>
""", unsafe_allow_html=True)


# 🔥 UI START
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.markdown('<div class="title">🚀 JobBuddy AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Find the best jobs tailored to your resume using AI</div>', unsafe_allow_html=True)


# 📤 Upload Resume
st.markdown('<div class="glass">', unsafe_allow_html=True)
st.markdown('<div class="label">📤 Upload Resume</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["pdf"])
st.markdown('</div>', unsafe_allow_html=True)


# 💼 Job Title
st.markdown('<div class="glass">', unsafe_allow_html=True)
st.markdown('<div class="label">💼 Job Title</div>', unsafe_allow_html=True)
job_title = st.text_input("", placeholder="e.g. Data Analyst")
st.markdown('</div>', unsafe_allow_html=True)


# 📧 Email
st.markdown('<div class="glass">', unsafe_allow_html=True)
st.markdown('<div class="label">📧 Email</div>', unsafe_allow_html=True)
email = st.text_input("", placeholder="your@email.com")
st.markdown('</div>', unsafe_allow_html=True)


# 🚀 BUTTON
find = st.button("🚀 Find Jobs")

st.markdown('</div>', unsafe_allow_html=True)


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

                if not job.get("link") or job["link"] == "#":
                    continue

                matched_jobs.append({
                    "title": clean_html(job["title"]),
                    "company": clean_html(job["company"]),
                    "score": score,
                    "link": job["link"]
                })

            matched_jobs = sorted(matched_jobs, key=lambda x: x["score"], reverse=True)

        st.markdown("## 🎯 Top Results")

        for job in matched_jobs[:10]:
            st.markdown(f"### {job['title']}")
            st.caption(job["company"])
            st.success(f"Match Score: {job['score']:.2f}%")
            st.link_button("🚀 Apply Now", job["link"])
            st.markdown("---")

        send_email(matched_jobs[:10], receiver=email)
        st.success("📩 Jobs sent to your email!")