# SQL Data Quality Results

The SQL checks compare the September 2026 and October 2026 job-posting releases to identify data quality issues and determine whether the October release is safe to ship.

## 1. Release Profile

| Check | September 2026 | October 2026 |
|---|---:|---:|
| Total postings | 650 | 632 |
| Missing titles | 0 (0%) | 14 (2.22%) |
| Missing salary | 122 (18.77%) | 97 (15.35%) |
| Missing closed date | 485 (74.62%) | 453 (71.68%) |

### Findings

The October release contains 632 postings compared with 650 in September.

Missing titles are a data quality problem because the job title is an important field for identifying and analysing a posting. September had no missing titles, while October had 14.

Missing salary values were found in both releases. I did not treat these as an error because salary information is not always available for every job posting.

Most postings also have no `closed_date`. This is expected because an empty `closed_date` can mean that the job is still open.

## 2. Duplicate Postings

I treated postings as duplicates when they had the same:

- `company_id`
- `title`
- `country_code`
- `city`
- `posted_date`

I did not use `posting_id` because it is unique for every row.

### Results

| Release | Duplicate groups |
|---|---:|
| September 2026 | 5 |
| October 2026 | 16 |

Each duplicate group appeared twice, so this represents 5 extra duplicate rows in September and 16 extra duplicate rows in October.

### Finding

The October release has more duplicate postings than September.

Duplicate postings can inflate job counts and affect analysis if the same job is counted more than once.

## 3. Missing Company Links

I checked whether every `company_id` in `job_postings` had a matching record in the `companies` table.

### Results

| Release | Missing company links |
|---|---:|
| September 2026 | 0 |
| October 2026 | 9 |

### Finding

Nine October job postings reference company IDs that do not exist in the `companies` table.

This is a data quality problem because those postings cannot be linked to valid company information. It can also cause missing or incorrect results when the job and company tables are joined.

## 4. Impossible Values

I checked for dates and salary values that do not make logical sense.

### Results

| Check | September 2026 | October 2026 |
|---|---:|---:|
| Posted after release snapshot date | 0 | 7 |
| Closed before posted date | 0 | 6 |
| `salary_min` greater than `salary_max` | 0 | 5 |
| Negative salary values | 0 | 2 |

### Findings

The October release contains several impossible values.

Seven postings have a `posted_date` after the October 1 snapshot date, which means they appear to have been posted after the release was created.

Six postings have a `closed_date` earlier than their `posted_date`.

Five postings have a minimum salary greater than the maximum salary.

Two postings contain negative salary values.

These issues can affect reporting and analysis because they create invalid dates and salary ranges.

## 5. Inconsistent Formats

I checked whether country codes, currency codes, job titles and company names followed consistent formats.

### Results

- 14 October records had inconsistent `country_code` values.
- No inconsistent currency formats were found.
- No title differences caused only by capitalization or extra spaces were found.
- Two company records normalized to the same name: `Kilima Tech`.

### Findings

The October release contains inconsistent country codes for Kenya, including values such as `ke`, `KEN` and `Kenya` instead of the expected two-letter uppercase code `KE`.

This can affect country-level analysis because records for the same country may be split across different values.

For company names, two records normalized to `kilima tech`:

- `Kilima Tech`
- ` kilima tech`

However, the two records have different company IDs and different industries, so I treated this as a formatting and possible entity-resolution issue rather than assuming they are definitely the same company.

No formatting problems were found in the non-empty currency values, and no title variations caused only by capitalization or extra spaces were found.

## 6. Salary Outliers

I checked for salaries that were far outside the typical range for other postings using the same currency.

For each release and currency, I calculated the average salary midpoint using:

`(salary_min + salary_max) / 2`

I then flagged postings whose salary midpoint was more than three times the average for that currency.

### Results

The October release contained 7 salary outliers:

- 4 postings using KES
- 3 postings using USD

No salary outliers were found in the September release using this threshold.

### Finding

These values are unusually high compared with other postings using the same currency.

I treated them as suspicious values that need investigation rather than automatically assuming they are incorrect, because unusually high salaries can sometimes be valid.

The three-times-average threshold was used as a simple rule to identify values that were far from the typical salary range.

## 7. Release Comparison

I compared the number of job postings by country between the September and October releases and calculated the percentage change.

### Results

Nigeria had the largest change:

| Country | September 2026 | October 2026 | Percentage change |
|---|---:|---:|---:|
| NG | 93 | 55 | -40.86% |

This was the only country in the comparison that changed by more than 20%.

### Investigation

I then checked the sources contributing Nigerian job postings.

In September:

- `company_site`: 26
- `jobboard_a`: 30
- `jobboard_b`: 37

In October:

- `company_site`: 16
- `jobboard_a`: 39
- `jobboard_b`: 0

`jobboard_b` was still supplying postings for other countries in October, so it did not stop working completely.

However, Nigerian postings from `jobboard_b` dropped from 37 to 0.

### Finding

The 40.86% drop in Nigerian postings may be related to a Nigeria-specific collection or coverage issue from `jobboard_b`.

This should be investigated before relying on the October Nigerian job counts.

I also found that some October Kenya records used inconsistent country values such as `ke`, `KEN` and `Kenya`, which can make country-level comparisons inaccurate if the values are not normalized first.