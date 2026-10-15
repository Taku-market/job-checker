# Job Checker

A small Python tool that fetches the latest job postings from the
[Arbeitnow](https://www.arbeitnow.com/) public API, scores each one with a set of
transparent keyword rules, and prints the top 10 QA / test-related roles — each with the
reasons behind its score.

Built as a QA automation practice project: the scoring logic is isolated in its own module
and covered by a 19-test pytest suite.

## Example output

```
[5] Senior ML Engineer | Kimchi (LLM Inference Optimization) / Kimchi  (skills,visa)
[4] Software Engineer, Robot Autonomy (Reliability & Test Infrastructure) / Laelaps  (qa role,skills)
[3] Security Engineer (Hybrid or Remote) / Vivid  (visa)
[2] Telecoms QA Director / netcracker  (qa role)
```

## How the score works

| Rule | Checked in | Points | Reason label |
|---|---|---|---|
| Mentions visa sponsorship | description | +3 | `visa` |
| Mentions Playwright, pytest, Python or Cypress | description | +2 | `skills` |
| Requires German (e.g. *German language*, *fluent in German*, *Deutschkenntnisse*, *fließend Deutsch*) | description | −3 | `language` |
| QA-type role (`qa`, `sdet`, `quality`, `test`) | title | +2 | `qa role` |

- Matching is case-insensitive (both title and description are lower-cased first).
- `score_job()` returns `(score, reasons)`, with reasons sorted alphabetically so the order
  is part of the spec rather than an accident of rule order.

## Project structure

| File | Role |
|---|---|
| `scoring.py` | `score_job(job)` — the scoring rules. Pure function, no network access |
| `check_API.py` | Fetches 250 postings from the API, scores them, prints the top 10 |
| `test_scoring.py` | pytest suite for `score_job` |

## Running it

```
pip install requests pytest
python check_API.py        # live run against the API
python -m pytest -v        # run the tests (no network needed)
```

## Tests

19 tests covering every rule:

| Area | Tests | What is checked |
|---|---|---|
| Visa | 1 | +3 |
| Skills | 4 | each keyword gives +2 (parametrized) |
| German requirement | 7 | each phrase gives −3 (parametrized) |
| "Germany" alone | 1 | the country name must **not** trigger the German penalty |
| QA role | 4 | each title keyword gives +2 (parametrized) |
| Combination | 1 | visa + skills = 5, reasons `["skills", "visa"]` |
| No match | 1 | 0 points, no reasons |

Notes on how the suite was built:

- **Isolated from the network.** `score_job` lives in its own module that never imports
  `requests`, so importing it in tests doesn't trigger an API call. The suite runs in ~0.03s.
- **Regression test for a real bug.** The first version of the German rule simply checked
  for `"german"`, which also matched the substring in *Germany* — the country name appears in
  almost every posting on a German job board. That flagged 112 of 250 postings, ~106 of them
  false positives. `test_germany_country_is_not_penalized` now guards against it coming back.
- **Mutation-checked.** I deliberately broke the code (restored the old `"german"` rule;
  removed `.lower()` from title and description) and confirmed the right tests fail. This
  showed that all-lowercase test inputs couldn't catch a missing `.lower()`, so the inputs now
  use realistic capitalisation (`Playwright`, `Visa`, `Deutschkenntnisse`, `QA`).
- **Positive and negative tests together.** "Should match" tests catch rules that are too
  strict; "should not match" tests catch rules that are too loose. Each bug above was caught by
  only one of the two kinds.

## Tuning the German rule: precision vs. recall

Measured against the same 250 postings, where about 14 actually required German:

| Version | Caught | Missed | False positives |
|---|---|---|---|
| `"german"` substring | 112 | ~0 | ~106 |
| 3 English phrases | 4 | 10 | ~0 |
| + `deutschkenntnisse` | 8 | 6 | ~0 |
| + more phrases (accidentally dropped one — a regression) | 10 | 4 | ~0 |
| Final | 13 | 1 | ~0 |

The one remaining miss (*"Very good German and English language skills"*) was accepted
rather than chased with an over-specific rule.

## Known limitations

- **One number mixes two different things.** The score adds *relevance* (QA role, skills)
  and *eligibility* (visa, German requirement) together, so an unrelated posting with 0 points
  can outrank a QA role that requires German (−1). A possible fix is to exclude
  German-required postings instead of penalising them, or report the two separately.
- `quality` also matches non-software roles (e.g. *Manufacturing Quality Engineer*).
- The API data can contain duplicate postings, which are not removed yet.

## Data source

Job data comes from the free [Arbeitnow Job Board API](https://www.arbeitnow.com/blog/job-board-api).
Please use it gently — the API asks not to be abused.
