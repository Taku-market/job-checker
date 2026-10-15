def score_job(job):
    score = 0
    items = []
    description = job["description"].lower()
    title = job["title"].lower()
    if "visa" in description:
        score += 3
        items.append("visa")

    if ("playwright" in description) or ("pytest" in description) or ("python" in description) or ("cypress" in description):
        score += 2
        items.append("skills")

    if ("german language" in description) or ("fluent in german" in description) or ("fluent german" in description) or ("german skills" in description) or ("deutschkenntnisse" in description) or ("fließend deutsch" in description) or ("fließendes deutsch" in description):
        score -=3
        items.append("language")

    if ("qa" in title) or ("sdet" in title) or ("quality" in title) or ("test" in title) :
        score +=2
        items.append("qa role")

    return score, sorted(items)


