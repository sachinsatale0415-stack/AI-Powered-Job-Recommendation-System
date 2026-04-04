import streamlit as st
import requests
from tavily import TavilyClient

# 🔐 CORRECT API KEYS
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
ADZUNA_APP_ID = st.secrets["ADZUNA_APP_ID"]
ADZUNA_APP_KEY = st.secrets["ADZUNA_APP_KEY"]

tavily = TavilyClient(api_key=TAVILY_API_KEY)


# 🔹 FETCH FROM TAVILY (FILTER BULK / LIST PAGES)
def fetch_from_tavily(job_title):
    query = f"{job_title} fresher OR entry level OR junior jobs India"

    try:
        response = tavily.search(query=query, max_results=10)
    except Exception as e:
        print("Tavily Error:", e)
        return []

    jobs = []

    for r in response.get("results", []):
        title = r.get("title", "").lower()

        # ❌ REMOVE BULK / AGGREGATED PAGES
        if any(x in title for x in [
            "jobs", "vacancies", "hiring", "list",
            "100", "200", "50", "openings"
        ]):
            continue

        jobs.append({
            "title": r.get("title", "Unknown Role"),
            "company": "From Web",
            "description": r.get("content", ""),
            "link": r.get("url", "#")
        })

    return jobs


# 🔹 FETCH FROM ADZUNA (BEST SOURCE)
def fetch_from_adzuna(job_title):
    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": 15,
        "what": job_title + " fresher",
        "where": "india",
        "content-type": "application/json"
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        # 🔥 DEBUG (VERY IMPORTANT)
        print("Adzuna Status:", response.status_code)

        data = response.json()
    except Exception as e:
        print("Adzuna Error:", e)
        return []

    jobs = []

    for j in data.get("results", []):
        description = j.get("description", "").lower()

        # 🔥 FILTER SENIOR JOBS
        if any(x in description for x in [
            "3+ years", "5+ years", "7+ years",
            "senior", "lead", "manager"
        ]):
            continue

        jobs.append({
            "title": j.get("title", "Unknown Role"),
            "company": j.get("company", {}).get("display_name", "Unknown"),
            "description": j.get("description", ""),
            "link": j.get("redirect_url", "#")
        })

    return jobs


# 🔹 MAIN FUNCTION
def fetch_jobs(job_title):
    try:
        adzuna_jobs = fetch_from_adzuna(job_title)
    except Exception as e:
        print("Adzuna Fetch Error:", e)
        adzuna_jobs = []

    try:
        tavily_jobs = fetch_from_tavily(job_title)
    except Exception as e:
        print("Tavily Fetch Error:", e)
        tavily_jobs = []

    # 🔥 COMBINE BOTH
    all_jobs = adzuna_jobs + tavily_jobs

    # 🔥 REMOVE DUPLICATES
    unique_jobs = []
    seen_titles = set()

    for job in all_jobs:
        title = job["title"].lower()

        if title not in seen_titles:
            seen_titles.add(title)
            unique_jobs.append(job)

    return unique_jobs