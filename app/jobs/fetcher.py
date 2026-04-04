import requests
from tavily import TavilyClient

# 🔐 ADD YOUR API KEYS
TAVILY_API_KEY = "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"
ADZUNA_APP_ID = "85744f45"
ADZUNA_APP_KEY = "0759887ee17572a6515252855569f2ce"

tavily = TavilyClient(api_key=TAVILY_API_KEY)


# 🔹 FETCH FROM TAVILY (FILTER BULK / LIST PAGES)
def fetch_from_tavily(job_title):
    query = f"{job_title} fresher OR entry level OR junior jobs India"

    try:
        response = tavily.search(query=query, max_results=10)
    except:
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
            "company": "Unknown",
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
        "results_per_page": 15,   # 🔥 more jobs
        "what": job_title + " fresher",   # 🔥 important
        "where": "india",
        "content-type": "application/json"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
    except:
        return []

    jobs = []

    for j in data.get("results", []):
        description = j.get("description", "").lower()

        # 🔥 OPTIONAL: FILTER SENIOR JOBS EARLY
        if any(x in description for x in [
            "3+ years", "5+ years", "7+ years",
            "senior", "lead", "manager"
        ]):
            continue

        jobs.append({
            "title": j.get("title", "Unknown Role"),
            "company": j.get("company", {}).get("display_name", "Unknown"),
            "description": j.get("description", ""),
            "link": j.get("redirect_url", "#")   # ✅ real apply link
        })

    return jobs


# 🔹 MAIN FUNCTION
def fetch_jobs(job_title):
    try:
        adzuna_jobs = fetch_from_adzuna(job_title)
    except:
        adzuna_jobs = []

    try:
        tavily_jobs = fetch_from_tavily(job_title)
    except:
        tavily_jobs = []

    # 🔥 PRIORITY: Adzuna first (better quality)
    all_jobs = adzuna_jobs + tavily_jobs

    # 🔥 REMOVE DUPLICATES (by title)
    unique_jobs = []
    seen_titles = set()

    for job in all_jobs:
        title = job["title"].lower()

        if title not in seen_titles:
            seen_titles.add(title)
            unique_jobs.append(job)

    return unique_jobs