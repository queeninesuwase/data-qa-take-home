# October 2026 Release Decision

## Release Decision: NO

I would not ship the October 2026 release in its current state.

- 14 postings are missing job titles.
- 9 postings cannot be linked to a valid company.
- Several records contain impossible dates or salary values.
- 16 duplicate posting groups were found in October.
- Nigerian postings dropped by 40.86%, with `jobboard_b` contributing no Nigerian records in October.

## Key Findings

| Issue | Count | Impact | Recommended Fix | Prevention |
|---|---:|---|---|---|
| Missing job titles | 14 | Postings cannot be reliably identified or grouped by role. | Recover the missing titles from the source or remove the affected records until corrected. | Validate required fields before publishing a release. |
| Missing company links | 9 | Job postings cannot be connected to valid company information. | Correct the `company_id` values or add the missing company records. | Add referential-integrity checks before release. |
| Duplicate postings | 16 duplicate groups | Job counts may be inflated because the same posting can be counted more than once. | Review and remove confirmed duplicates. | Run duplicate checks before publishing each release. |
| Invalid dates | 13 | 7 postings are dated after the snapshot and 6 close before they were posted, making timeline analysis unreliable. | Correct the affected dates using source data. | Add date-order and snapshot-date validation rules. |
| Invalid salary values | 7 | 5 salary ranges have minimum values above maximum values and 2 contain negative salaries. | Correct the affected salary fields using source data. | Validate salary ranges and reject negative values during ingestion. |
| Inconsistent country codes | 14 | Kenya records can be split between `KE`, `ke`, `KEN` and `Kenya`, affecting country-level counts. | Normalize the values to the expected two-letter country code. | Standardize and validate country codes during ingestion. |
| Salary outliers | 7 | Extremely high values may distort salary averages and other analysis. | Review the records against their original sources before changing them. | Add automated outlier monitoring by currency. |
| Large Nigeria release drop | -40.86% | Nigerian job counts may be incomplete in October. | Investigate why `jobboard_b` supplied 37 Nigerian postings in September but 0 in October. | Add release-over-release monitoring by country and source. |

## Correctness Rules

1. **Block release if required job titles are missing.**  
   A job posting without a title should not be published because it cannot be reliably identified or analysed.

2. **Block release if a posting references a company that does not exist.**  
   Every `company_id` in `job_postings` should match a record in the `companies` table.

3. **Block release if dates or salary ranges are impossible.**  
   A posting should not have a future `posted_date` relative to the snapshot, a `closed_date` before `posted_date`, a negative salary, or `salary_min` greater than `salary_max`.

4. **Warn if duplicate postings are detected.**  
   Duplicate groups should be reviewed before release because they can inflate job counts, but they may sometimes represent the same role collected from different sources.

5. **Warn if a country changes by more than 20% between releases.**  
   Large changes should be investigated by country and source before publication to make sure they are real changes and not collection problems.