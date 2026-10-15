import requests
from scoring import score_job

response = requests.get("https://www.arbeitnow.com/api/job-board-api")
data = response.json()
jobs = data["data"]
results = []

for job in jobs:
    title = job["title"].lower()
    score, items = score_job(job)
    reasons = ",".join(items)
    if ("qa" in title) or ("quality" in title) or ("engineer" in title):
        results.append((score, job["title"], job["company_name"],reasons))

results.sort(reverse=True)
for score, title, company, reasons in results[:10]:
    print(f"[{score}] {title} / {company}  ({reasons})")
