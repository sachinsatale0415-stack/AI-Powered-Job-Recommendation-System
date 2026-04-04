import streamlit as st
import requests
import re
from tavily import TavilyClient

# 🔐 API KEYS
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
ADZUNA_APP_ID = st.secrets["ADZUNA_APP_ID"]
ADZUNA_APP_KEY = st.secrets["ADZUNA_APP_KEY"]

tavily = TavilyClient(api_key=TAVILY_API_KEY)


# 🔥 CLEAN HTML FUNCTION
def clean_html(text):
    if not text:
        return ""
    return re.sub('<.*?>', '', text)


# 🔹 FETCH FROM TAVILY (CLEANED)
def fetch_from_tavily(job_title):
    query = f"{job_title} fresher OR entry level OR junior jobs India"

    try:
        response = tavily.search(query=query, max_results=10)
        print("Tavily Results:", len(response.get("results", [])))
    except Exception as e:
        print("Tavily Error:", e)
        return []

    jobs = []

    for r in response.get("results", []):
        title = clean_html(r.get("title", "")).lower()
        url = r.get("url", "")

        # ❌ REMOVE AGGREGATED / LISTING PAGES
        if any(x in title for x in [
            "jobs in", "jobs -", "jobs |", "vacancies",
            "glassdoor", "linkedin jobs", "naukri jobs",
            "wellfound", "foundit", "list of jobs"
        ]):
            continue

        # ❌ REMOVE INVALID LINKS
        if not url or "jobs" in url and "search" in url:
            continue

        jobs.append({
            "title": clean_html(r.get("title", "Unknown Role")),
            "company": "From Web",
            "description": "",  # 🔥 REMOVE DIRTY CONTENT COMPLETELY
            "link": url
        })

    return jobs


# 🔹 FETCH FROM ADZUNA (BEST SOURCE)
def fetch_from_adzuna(job_title):
    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": 15,
        "what": job_title,
        "where": "India"
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        print("Adzuna Status:", response.status_code)

        if response.status_code != 200:
            print("Adzuna Error:", response.text)
            return []

        data = response.json()
        results = data.get("results", [])

        print("Adzuna Jobs Found:", len(results))

    except Exception as e:
        print("Adzuna Exception:", e)
        return []

    jobs = []

    for j in results:
        description = clean_html(j.get("description", "").lower())

        # ❌ REMOVE SENIOR ROLES
        if any(x in description for x in [
            "7+ years", "10+ years", "senior manager"
        ]):
            continue

        jobs.append({
            "title": clean_html(j.get("title", "Unknown Role")),
            "company": clean_html(j.get("company", {}).get("display_name", "Unknown")),
            "description": description,
            "link": j.get("redirect_url", "#")
        })

    return jobs


# 🔹 REMOVE DUPLICATES
def remove_duplicates(jobs):
    unique_jobs = []
    seen = set()

    for job in jobs:
        key = (job["title"].lower(), job["company"].lower())

        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)

    return unique_jobs


# 🔹 MAIN FUNCTION
def fetch_jobs(job_title):
    print(f"\nFetching jobs for: {job_title}")

    adzuna_jobs = fetch_from_adzuna(job_title)
    tavily_jobs = fetch_from_tavily(job_title)

    all_jobs = adzuna_jobs + tavily_jobs

    print("Before Dedup:", len(all_jobs))

    unique_jobs = remove_duplicates(all_jobs)

    print("Final Jobs:", len(unique_jobs))

    return unique_jobs