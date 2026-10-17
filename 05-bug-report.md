# Bug Report

## Title

Nigeria job postings from `jobboard_b` are missing in the October 2026 release

## Location

`job_postings` table, October 2026 release, Nigeria (`NG`).

## Query Used

```sql
SELECT
    release,
    source,
    COUNT(*) AS posting_count
FROM job_postings
WHERE country_code = 'NG'
GROUP BY release, source
ORDER BY release, source;