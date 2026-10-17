```text
workforce-data-quality-validation/
├── 01-api-tests/
│   ├── conftest.py
│   ├── test_countries_api.py
│   └── findings.md
├── 02-sql-checks/
│   ├── checks.sql
│   └── results.md
├── 03-data-tests/
│   ├── conftest.py
│   └── test_data_quality.py
├── data/
│   ├── companies.csv
│   ├── job_postings.csv
│   └── revelio_practice.db
├── 04-write-up.md
├── 05-bug-report.md
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv env
source env/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## API Tests

The API tests use the REST Countries API.

The current API version requires an API key, so I used an environment variable instead of storing the key in the project.

Set the API key:

```bash
export REST_COUNTRIES_API_KEY="your_api_key"
```

Run the API tests:

```bash
python -m pytest 01-api-tests/ -v
```

The tests cover successful requests, invalid inputs, edge cases and basic data sanity checks.

## SQL Data Quality Checks

The SQL checks are stored in `02-sql-checks/checks.sql`.

They check:

- release size and missing values
- duplicate postings
- missing company links
- impossible dates
- invalid salary ranges
- negative salaries
- inconsistent formats
- salary outliers
- release-over-release changes

The results are documented in `02-sql-checks/results.md`.

## Automated Data Tests

Run the automated data-quality tests with:

```bash
python -m pytest 03-data-tests/ -v
```

Known issues in the October release are marked with `xfail`.

## Release Decision

I would not ship the October 2026 release in its current state.

The release contains missing titles, missing company links, duplicate postings, invalid dates and salary values, inconsistent country codes and a large drop in Nigerian job postings that needs investigation.

More details are in `04-write-up.md`.

## Bug Report

The main issue investigated was the disappearance of Nigerian postings from `jobboard_b` in the October release.

The full bug report is in `05-bug-report.md`.
