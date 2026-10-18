import pytest
from scoring import score_job, requires_german

@pytest.mark.parametrize("keyword", [
    "Playwright",
    "Pytest", 
    "Python",
    "Cypress"
    ])
def test_skills_keywords(keyword):
    job = {
        "title": "Sales Manager",
        "description": f"Experience with {keyword} required",
    }
    score, items = score_job(job)
    assert score == 2
    assert items == ["skills"]

def test_visa_job():
    job = {
        "title": "Sales Manager",
        "description": "We offer Visa sponsorship",
    }
    score, items = score_job(job)
    assert score == 3
    assert items == ["visa"]

def test_germany_country_is_not_penalized():
    job = {
        "title": "Sales Manager",
        "description": "Location is in Germany",
    }
    assert requires_german(job) is False

@pytest.mark.parametrize("phrase", [
    "German language", 
    "Fluent in german", 
    "Fluent german", 
    "German skills", 
    "Deutschkenntnisse", 
    "Fließend deutsch", 
    "Fließendes deutsch"
])
def test_phrase_job(phrase):
    job = {
        "title": "Sales Manager",
        "description": f"This position required {phrase}",
    }
    assert requires_german(job) is True

@pytest.mark.parametrize("title", [
    "QA",
    "SDET",
    "QUALITY",
    "TEST",
])
def test_job_title(title):
    job = {
        "title": f"{title}",
        "description": "This position required over 3 years exprienced",
    }
    score, items = score_job(job)
    assert score == 2
    assert items == ["qa role"]

def test_visa_and_skills():
    job = {
        "title": "Sales Manager",
        "description": "We require Python skills and offer Visa sponsorship",
    }
    score, items = score_job(job)
    assert score == 5
    assert items == ["skills", "visa"]

def test_no_match():
    job = {
        "title": "Sales manager",
        "description": "Required managing vendor over 3 years experienced",
    }
    score, items = score_job(job)
    assert score == 0
    assert items == []