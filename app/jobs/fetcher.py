import streamlit as st
import requests
from tavily import TavilyClient

# 🔐 API KEYS
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
ADZUNA_APP_ID = st.secrets["ADZUNA_APP_ID"]
ADZUNA_APP_KEY = st.secrets["ADZUNA_APP_KEY"]

tavily = TavilyClient(api_key=TAVILY_API_KEY)


# 🔹 FETCH FROM TAVILY
def fetch_from_tavily(job_title):
    query = f"{job_title} fresher OR entry level OR junior jobs India"

    try:
        response = tavily.search(query=query, max_results=10)
        print("Tavily Raw Results:", len(response.get("results", [])))
    except Exception as e:
        print("❌ Tavily Error:", e)
        return []

    jobs = []

    for r in response.get("results", []):
        title = r.get("title", "").lower()

        # ❗ Only remove obvious bulk pages
        if any(x in title for x in ["100", "200", "bulk hiring"]):
            continue

        jobs.append({
            "title": r.get("title", "Unknown Role"),
            "company": "From Web",
            "description": r.get("content", ""),
            "link": r.get("url", "#")
        })

    print("✅ Tavily Clean Jobs:", len(jobs))
    return jobs


# 🔹 FETCH FROM ADZUNA (MAIN SOURCE)
def fetch_from_adzuna(job_title):
    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": 15,
        "what": job_title,   # 🔥 removed "fresher" for broader results
        "where": "India"
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        print("\n🔵 Adzuna Status:", response.status_code)
        print("🔗 URL:", response.url)

        if response.status_code != 200:
            print("❌ Adzuna Error Response:", response.text)
            return []

        data = response.json()
        results = data.get("results", [])

        print("📊 Total Jobs Found:", len(results))

    except Exception as e:
        print("❌ Adzuna Exception:", e)
        return []

    jobs = []

    for j in results:
        description = j.get("description", "").lower()

        # ✅ Light filtering (not aggressive)
        if "7+ years" in description or "10+ years" in description:
            continue

        jobs.append({
            "title": j.get("title", "Unknown Role"),
            "company": j.get("company", {}).get("display_name", "Unknown"),
            "description": j.get("description", ""),
            "link": j.get("redirect_url", "#")
        })

    print("✅ Adzuna Clean Jobs:", len(jobs))
    return jobs


# 🔹 REMOVE DUPLICATES (IMPROVED)
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
    print(f"\n🚀 Fetching jobs for: {job_title}")

    adzuna_jobs = fetch_from_adzuna(job_title)
    tavily_jobs = fetch_from_tavily(job_title)

    all_jobs = adzuna_jobs + tavily_jobs

    print("🔄 Total Before Dedup:", len(all_jobs))

    unique_jobs = remove_duplicates(all_jobs)

    print("✅ Final Jobs After Dedup:", len(unique_jobs))

    return unique_jobs