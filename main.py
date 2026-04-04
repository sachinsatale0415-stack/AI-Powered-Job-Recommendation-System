from app.resume.parser import extract_text_from_pdf
from app.jobs.fetcher import fetch_jobs
from app.matching.matcher import calculate_match
from app.notifications.email import send_email

if __name__ == "__main__":
    # 🔹 Extract resume text
    text = extract_text_from_pdf("resume.pdf")

    # 🔹 Fetch jobs
    jobs = fetch_jobs()

    matched_jobs = []

    for job in jobs:
        # 🔥 AI-based matching
        score = calculate_match(text, job["description"])

        # 🔥 Improved fresher detection
        is_fresher = any(
            x in job["description"].lower()
            for x in ["fresher", "0-1", "0 to 1", "entry level", "junior"]
        )

        # 🔥 Flexible filtering (IMPORTANT FIX)
        if score >= 50 or is_fresher:
            matched_jobs.append({
                "title": job["title"],
                "company": job["company"],
                "score": score,
                "link": job.get("link", "No link available")
            })

    # 🔥 SORT BY BEST MATCH
    matched_jobs = sorted(matched_jobs, key=lambda x: x["score"], reverse=True)

    print("\n===== TOP MATCHED JOBS =====")

    if not matched_jobs:
        print("\n❌ No matching jobs found")
    else:
        for job in matched_jobs:
            print(f"\n{job['title']} at {job['company']}")
            print(f"Match Score: {job['score']:.2f}%")
            print(f"Apply Here: {job['link']}")
            print("-" * 50)

        # 📩 Send top 10 jobs via email
        top_jobs = matched_jobs[:10]

        print(f"\n===== TOP {len(top_jobs)} JOBS SENT VIA EMAIL =====")

        for job in top_jobs:
            print(f"\n🔹 {job['title']} at {job['company']}")
            print(f"Match Score: {job['score']:.2f}%")
            print(f"Apply Here: {job['link']}")
            print("-" * 50)

        send_email(top_jobs)