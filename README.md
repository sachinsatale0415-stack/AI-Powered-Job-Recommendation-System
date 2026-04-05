# 🚀 JobBuddy AI — Smart Job Recommendation System

## 📌 Overview

JobBuddy AI is an intelligent job recommendation system designed to help fresh graduates find relevant job opportunities efficiently. It analyzes a candidate’s resume to understand their skills and matches them with suitable job listings from multiple platforms. Using AI-based scoring, the system ranks jobs based on relevance and filters out roles not suitable for freshers. The platform provides a clean, user-friendly interface along with email notifications for top job matches. Overall, it simplifies the job search process by making it faster, smarter, and more personalized.

## 🚧 Problem Statement

Fresh graduates often struggle to find job opportunities that match their skills and career interests. Most job portals provide generic listings without personalization, forcing candidates to manually search and filter through hundreds of roles.

Additionally, many listings require prior experience, making it difficult for freshers to identify suitable opportunities. This leads to wasted time, low application success rates, and frustration.

There is a need for an intelligent system that can analyze a candidate’s resume and recommend relevant, fresher-friendly jobs efficiently.

## 🎯 Objective of the Project

The primary objective of JobBuddy AI is to simplify and optimize the job search process for fresh graduates by leveraging artificial intelligence and automation.

This project aims to:

• 🔍 Analyze candidate resumes to understand their skills, domain, and interests

• 🤖 Automatically fetch relevant job opportunities from multiple platforms

• 🎯 Match candidate profiles with job descriptions using AI-based scoring

• 🚫 Filter out irrelevant or senior-level roles not suitable for freshers

• 📊 Rank job opportunities based on relevance and match percentage

• 📩 Provide personalized job recommendations directly to the user via UI and email

By achieving these objectives, the system reduces manual effort, improves job discovery efficiency, and increases the chances of freshers finding roles that truly match their skills and career goals.

## 💡 Solution / Approach

JobBuddy AI addresses the challenges faced by freshers by automating the job search process using an AI-driven approach. The system first extracts and processes text from the uploaded resume to identify key skills and domains. It then fetches job listings from multiple sources and cleans the data to remove irrelevant or duplicate entries.

Using semantic similarity techniques, the system compares the resume content with job descriptions and assigns a match score to each job. It further filters out senior-level roles and prioritizes fresher-friendly opportunities. Finally, the jobs are ranked based on relevance and presented to the user through an intuitive interface, along with email notifications for easy access.

## ✨ Features

• 📄 Resume Parsing (PDF)

• 🧠 AI-Based Job Matching

• 🌐 Job Fetching from APIs (Adzuna + Tavily)

• 🎯 Match Score Ranking

• 📩 Email Notifications

• ⚡ Clean Interactive UI (Streamlit)

## 🏗️ Architecture

• Frontend: Streamlit

• Backend: Python

• Resume Parsing: pdfplumber

• AI Matching: sentence-transformers

• Job APIs: Tavily + Adzuna

## 🔄 Workflow

1. Upload Resume

2. Extract Text

3. Fetch Jobs

4. Match Resume with Jobs

5. Rank by Score

6. Display Top Results

7. Send Email

## 🛠️ Tech Stack

• Python

• Streamlit

• NLP (Sentence Transformers)

• REST APIs

• AWS-ready architecture (scalable)

## 📸 UI Preview
<img width="1919" height="741" alt="image" src="https://github.com/user-attachments/assets/e4a3af38-e967-40fd-ba71-c831ede0a6c3" />

<img width="1919" height="787" alt="image" src="https://github.com/user-attachments/assets/c02380ae-fdb1-40a2-a4c3-022fc8fd2dfd" />

<img width="1919" height="738" alt="image" src="https://github.com/user-attachments/assets/cc773829-4f53-462f-b910-3f539556ec86" />

<img width="1919" height="792" alt="image" src="https://github.com/user-attachments/assets/05d370b2-3469-427a-a408-d5ffe3284b48" />

## 🚀 How to Run

git clone https://github.com/sachinsatale0415-stack/AI-Powered-Job-Recommendation-System

cd jobbuddy-ai

pip install -r requirements.txt

streamlit run app.py

## 🔐 Setup

Add API keys in .streamlit/secrets.toml:

TAVILY_API_KEY="your_key"

ADZUNA_APP_ID="your_id"

ADZUNA_APP_KEY="your_key"

## 📊 Results / Output
As soon as you upload the Resume, job title ans your email you will get the results and also get the email from my ai syatem whoes email is - jobbyddys.ai@gmail.com

<img width="1918" height="796" alt="image" src="https://github.com/user-attachments/assets/c0e6513d-28d0-482c-a04e-48095932d564" />

<img width="1919" height="745" alt="image" src="https://github.com/user-attachments/assets/a819ecf6-e9ed-4bf6-9faf-5ce3ef50c243" />

<img width="1913" height="805" alt="image" src="https://github.com/user-attachments/assets/11d87dea-1eab-46ac-bc20-e6c405bf54c1" />



## 🎯 Future Improvements

• LinkedIn API Integration

• Auto Apply Feature

• Resume Optimization Suggestions

• AI Career Guidance Bot

## 👨‍💻 Author

Sachin Satale

Aspiring AI Engineer | Data Analyst | ML Enthusiast
