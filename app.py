import streamlit as st
import tempfile
import base64

from app.resume.parser import extract_text_from_pdf
from app.jobs.fetcher import fetch_jobs
from app.matching.matcher import calculate_match
from app.notifications.email import send_email


# 🔥 PAGE CONFIG
st.set_page_config(page_title="Search Jobs with Piyu", layout="wide")


# 🔥 LOAD BACKGROUND IMAGE
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg_image = get_base64("assets/bg.png")


# 🔥 CUSTOM UI CSS
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
    color: white;
    font-size: 42px;
    font-weight: bold;
}}

.section {{
    background: rgba(0, 0, 0, 0.6);
    padding: 25px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    margin-bottom: 20px;
}}

.job-card {{
    background: rgba(0, 0, 0, 0.7);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    color: white;
    border: 1px solid rgba(0,255,255,0.3);
    transition: 0.3s;
}}

.job-card:hover {{
    transform: scale(1.02);
    box-shadow: 0px 0px 20px rgba(0,255,255,0.8);
}}

.apply-btn {{
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    padding: 10px 15px;
    border-radius: 10px;
    color: white;
    text-decoration: none;
    font-weight: bold;
}}
</style>
""", unsafe_allow_html=True)


# 🔥 HEADER
st.markdown('<div class="title">🚀 Search Jobs with Piyu </div>', unsafe_allow_html=True)
st.write("")


# 🔹 INPUT SECTION
st.markdown('<div class="section">', unsafe_allow_html=True)

st.subheader("📤 Upload Your Resume")
uploaded_file = st.file_uploader("", type=["pdf"])

st.subheader("💼 Job Title")
job_title = st.text_input("", placeholder="Python Developer")

st.subheader("📧 Enter Your Email")
email = st.text_input("", placeholder="your@email.com")

st.markdown('</div>', unsafe_allow_html=True)


# 🔥 BUTTON
if st.button("🔍 Find Jobs"):

    if not uploaded_file or not email:
        st.warning("Please upload resume and enter email")

    else:
        with st.spinner("🤖 AI is analyzing your resume..."):

            # SAVE FILE
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                file_path = tmp.name

            # EXTRACT TEXT
            text = extract_text_from_pdf(file_path)

            # DEFAULT JOB TITLE
            if not job_title:
                job_title = "python developer"

            # FETCH JOBS
            jobs = fetch_jobs(job_title)

            matched_jobs = []

            for job in jobs:
                description = job["description"].lower()

                score = calculate_match(text, description)

                # 🔥 EXPERIENCE DETECTION
                is_fresher = any(x in description for x in [
                    "fresher", "0-1", "0 to 1", "entry level", "junior", "graduate"
                ])

                is_senior = any(x in description for x in [
                    "3+ years", "5+ years", "7+ years",
                    "senior", "lead", "manager"
                ])

                # ❌ REMOVE SENIOR JOBS
                if is_senior and not is_fresher:
                    continue

                # 🔥 BOOST FRESHER JOBS
                if is_fresher:
                    score += 15

                # 🔥 BOOST JOB TITLE MATCH
                if job_title.lower() in job["title"].lower():
                    score += 10

                matched_jobs.append({
                    "title": job["title"],
                    "company": job["company"],
                    "score": score,
                    "link": job.get("link", "#")
                })

            # 🔥 SORT BY HIGHEST SCORE
            matched_jobs = sorted(
                matched_jobs,
                key=lambda x: x["score"],
                reverse=True
            )

            # 🔥 TOP 10
            top_jobs = matched_jobs[:10]

            # 🔥 SHOW RESULTS
            st.markdown("## 🎯 Top Results")

            if not top_jobs:
                st.error("No suitable fresher jobs found 😢")

            else:
                for job in top_jobs:
                    st.markdown(f"""
                    <div class="job-card">
                        <h3>{job['title']}</h3>
                        <p><b>{job['company']}</b></p>
                        <p>✨ Match Score: {job['score']:.2f}%</p>
                        <a href="{job['link']}" target="_blank" class="apply-btn">
                            🚀 Apply Now
                        </a>
                    </div>
                    """, unsafe_allow_html=True)

                # 📩 SEND EMAIL
                send_email(top_jobs, receiver=email)

                st.success("📩 Jobs sent to your email!")
                st.balloons()