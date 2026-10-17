-- Count total job postings in each release
SELECT
    release,
    COUNT(*) AS total_postings
FROM job_postings
GROUP BY release;

-- Count postings with missing titles in each release
SELECT
    release,
    COUNT(*) AS missing_titles
FROM job_postings
WHERE title IS NULL OR title = ''
GROUP BY release;

-- Count postings with both salary fields missing
SELECT
    release,
    COUNT(*) AS missing_salary
FROM job_postings
WHERE salary_min IS NULL
  AND salary_max IS NULL
GROUP BY release;

-- Count postings with no closed date
SELECT
    release,
    COUNT(*) AS missing_closed_dates
FROM job_postings
WHERE closed_date IS NULL OR closed_date = ''
GROUP BY release;

-- Find possible duplicate postings within each release
SELECT
    release,
    company_id,
    title,
    country_code,
    city,
    posted_date,
    COUNT(*) AS times_found
FROM job_postings
GROUP BY
    release,
    company_id,
    title,
    country_code,
    city,
    posted_date
HAVING COUNT(*) > 1
ORDER BY release;

-- Find job postings whose company_id does not exist in the companies table
SELECT
    job_postings.release,
    job_postings.posting_id,
    job_postings.company_id
FROM job_postings
LEFT JOIN companies
    ON job_postings.company_id = companies.company_id
WHERE companies.company_id IS NULL;

-- Find postings dated after the release snapshot date
SELECT
    release,
    posting_id,
    posted_date
FROM job_postings
WHERE
    (release = '2026-09' AND posted_date > '2026-09-01')
    OR
    (release = '2026-10' AND posted_date > '2026-10-01');

-- Find postings that closed before they were posted
SELECT
    release,
    posting_id,
    posted_date,
    closed_date
FROM job_postings
WHERE closed_date IS NOT NULL
  AND closed_date != ''
  AND closed_date < posted_date;

-- Find salary ranges where the minimum is greater than the maximum
SELECT
    release,
    posting_id,
    salary_min,
    salary_max
FROM job_postings
WHERE salary_min IS NOT NULL
  AND salary_max IS NOT NULL
  AND salary_min > salary_max;

-- Find postings with negative salary values
SELECT
    release,
    posting_id,
    salary_min,
    salary_max
FROM job_postings
WHERE salary_min < 0
   OR salary_max < 0;

-- Find country codes that are not two uppercase characters
SELECT
    release,
    posting_id,
    country_code
FROM job_postings
WHERE country_code IS NOT NULL
  AND (
      LENGTH(country_code) != 2
      OR country_code != UPPER(country_code)
  );

-- Find currency values that are not three uppercase characters
SELECT
    release,
    posting_id,
    currency
FROM job_postings
WHERE currency IS NOT NULL
  AND currency != ''
  AND (
      LENGTH(currency) != 3
      OR currency != UPPER(currency)
  );

-- Find job titles that only differ by capitalization or extra spaces
SELECT
    LOWER(TRIM(title)) AS normalized_title,
    COUNT(DISTINCT title) AS different_versions
FROM job_postings
WHERE title IS NOT NULL
  AND title != ''
GROUP BY LOWER(TRIM(title))
HAVING COUNT(DISTINCT title) > 1;

-- Find company names that only differ by capitalization or extra spaces
SELECT
    LOWER(TRIM(company_name)) AS normalized_name,
    COUNT(DISTINCT company_name) AS different_versions
FROM companies
GROUP BY LOWER(TRIM(company_name))
HAVING COUNT(DISTINCT company_name) > 1;

-- Find salary outliers that are more than three times the average for their currency
WITH currency_average AS (
    SELECT
        release,
        currency,
        AVG((salary_min + salary_max) / 2.0) AS average_salary
    FROM job_postings
    WHERE salary_min IS NOT NULL
      AND salary_max IS NOT NULL
      AND salary_min >= 0
      AND salary_max >= 0
      AND salary_min <= salary_max
    GROUP BY release, currency
)
SELECT
    job_postings.release,
    job_postings.posting_id,
    job_postings.currency,
    job_postings.salary_min,
    job_postings.salary_max,
    ROUND(currency_average.average_salary, 2) AS average_salary
FROM job_postings
JOIN currency_average
    ON job_postings.release = currency_average.release
    AND job_postings.currency = currency_average.currency
WHERE job_postings.salary_min IS NOT NULL
  AND job_postings.salary_max IS NOT NULL
  AND job_postings.salary_min >= 0
  AND job_postings.salary_max >= 0
  AND job_postings.salary_min <= job_postings.salary_max
  AND ((job_postings.salary_min + job_postings.salary_max) / 2.0)
      > currency_average.average_salary * 3
ORDER BY job_postings.release, job_postings.currency;

-- Compare posting counts by country between September and October
WITH country_counts AS (
    SELECT
        country_code,
        SUM(CASE WHEN release = '2026-09' THEN 1 ELSE 0 END) AS september_count,
        SUM(CASE WHEN release = '2026-10' THEN 1 ELSE 0 END) AS october_count
    FROM job_postings
    GROUP BY country_code
)
SELECT
    country_code,
    september_count,
    october_count,
    ROUND(
        ((october_count - september_count) * 100.0) / september_count,
        2
    ) AS percentage_change
FROM country_counts
WHERE september_count > 0
ORDER BY ABS(
    ((october_count - september_count) * 100.0) / september_count
) DESC;

-- Compare Nigerian posting counts by source between releases
SELECT
    release,
    source,
    COUNT(*) AS posting_count
FROM job_postings
WHERE country_code = 'NG'
GROUP BY release, source
ORDER BY release, source;

-- Compare total posting counts by source between releases
SELECT
    release,
    source,
    COUNT(*) AS posting_count
FROM job_postings
GROUP BY release, source
ORDER BY release, source;

-- Check jobboard_b posting counts by country and release
SELECT
    release,
    country_code,
    COUNT(*) AS posting_count
FROM job_postings
WHERE source = 'jobboard_b'
GROUP BY release, country_code
ORDER BY country_code, release;