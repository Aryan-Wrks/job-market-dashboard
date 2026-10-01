import sqlite3
import requests
import json
import time

from config import LLM_API_KEY

DB_PATH = "jobs.db"
MODEL = "gemini-2.5-flash-lite"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"


def build_prompt(description):
    return (
        "Extract up to 5 technical skills required in this job description. "
        "Respond ONLY with a JSON array of strings, nothing else. "
        "Example: [\"Python\", \"SQL\", \"AWS\"]\n\n"
        f"Job description:\n{description}"
    )


def extract_skills(description, retries=3):
    payload = {
        "contents": [
            {"parts": [{"text": build_prompt(description)}]}
        ]
    }
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": LLM_API_KEY,
    }

    for attempt in range(1, retries + 1):
        response = requests.post(URL, headers=headers, json=payload, timeout=20)

        if response.status_code == 200:
            break
        elif response.status_code == 503 and attempt < retries:
            print(f"  Server busy, retrying in 5s (attempt {attempt}/{retries})...")
            time.sleep(5)
        else:
            print(f"  API error {response.status_code}: {response.text[:200]}")
            return []

    data = response.json()
    try:
        raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        print("  Unexpected response shape, skipping")
        return []

    cleaned = raw_text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        skills = json.loads(cleaned)
        if isinstance(skills, list):
            return [str(s).strip() for s in skills if s]
    except json.JSONDecodeError:
        print(f"  Could not parse JSON: {cleaned[:100]}")

    return []


def main():
    conn = sqlite3.connect(DB_PATH)

    # only process jobs that don't already have skills (safe to re-run)
    jobs = conn.execute("""
        SELECT job_id, description FROM jobs
        WHERE job_id NOT IN (SELECT DISTINCT job_id FROM skills)
    """).fetchall()[:5]

    print(f"Jobs needing skill extraction: {len(jobs)}")

    for i, (job_id, description) in enumerate(jobs, start=1):
        print(f"[{i}/{len(jobs)}] {job_id}")
        skills = extract_skills(description)

        for skill in skills:
            conn.execute(
                "INSERT OR IGNORE INTO skills (job_id, skill_name) VALUES (?, ?)",
                (job_id, skill),
            )
        conn.commit()

        time.sleep(10)  # be polite to the free tier rate limit

    conn.close()
    print("Done.")


if __name__ == "__main__":
    main()