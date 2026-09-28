import json
import glob

total = 0
with_salary = 0
desc_lengths = []
ids = set()

for path in glob.glob("data/raw/*.json"):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    for job in data["results"]:
        total += 1
        ids.add(job["id"])
        if job.get("salary_min") is not None:
            with_salary += 1
        desc_lengths.append(len(job.get("description", "")))

print("Total jobs across all files:", total)
print("Unique job ids:", len(ids))
print("Jobs with salary:", with_salary)
print("Average description length:", round(sum(desc_lengths) / len(desc_lengths)))
print("Longest description:", max(desc_lengths))