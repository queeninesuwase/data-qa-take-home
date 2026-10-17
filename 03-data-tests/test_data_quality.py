import pytest


@pytest.mark.xfail(reason="October release contains known missing titles")
def test_october_postings_have_titles(db_connection):
    cursor = db_connection.cursor()

    cursor.execute(
        """
        SELECT posting_id
        FROM job_postings
        WHERE release = '2026-10'
          AND (title IS NULL OR title = '')
        """
    )

    rows = cursor.fetchall()
    example_ids = [row[0] for row in rows[:5]]

    assert len(rows) == 0, (
        f"Found {len(rows)} postings with missing titles. "
        f"Example posting IDs: {example_ids}"
    )

@pytest.mark.xfail(reason="October release contains postings with missing company links")
def test_october_postings_have_valid_company_links(db_connection):
    cursor = db_connection.cursor()

    cursor.execute(
        """
        SELECT job_postings.posting_id
        FROM job_postings
        LEFT JOIN companies
            ON job_postings.company_id = companies.company_id
        WHERE job_postings.release = '2026-10'
          AND companies.company_id IS NULL
        """
    )

    rows = cursor.fetchall()
    example_ids = [row[0] for row in rows[:5]]

    assert len(rows) == 0, (
        f"Found {len(rows)} postings with missing company links. "
        f"Example posting IDs: {example_ids}"
    )

@pytest.mark.xfail(reason="October release contains salary ranges where minimum is greater than maximum")
def test_october_salary_ranges_are_valid(db_connection):
    cursor = db_connection.cursor()

    cursor.execute(
        """
        SELECT posting_id
        FROM job_postings
        WHERE release = '2026-10'
          AND salary_min IS NOT NULL
          AND salary_max IS NOT NULL
          AND salary_min > salary_max
        """
    )

    rows = cursor.fetchall()
    example_ids = [row[0] for row in rows[:5]]

    assert len(rows) == 0, (
        f"Found {len(rows)} postings with invalid salary ranges. "
        f"Example posting IDs: {example_ids}"
    )

@pytest.mark.xfail(reason="October release contains postings dated after the snapshot date")
def test_october_postings_are_not_future_dated(db_connection):
    cursor = db_connection.cursor()

    cursor.execute(
        """
        SELECT posting_id
        FROM job_postings
        WHERE release = '2026-10'
          AND posted_date > '2026-10-01'
        """
    )

    rows = cursor.fetchall()
    example_ids = [row[0] for row in rows[:5]]

    assert len(rows) == 0, (
        f"Found {len(rows)} postings dated after the October snapshot date. "
        f"Example posting IDs: {example_ids}"
    )

@pytest.mark.xfail(reason="Nigeria posting count dropped by more than 20% in October")
def test_nigeria_release_change_is_within_20_percent(db_connection):
    cursor = db_connection.cursor()

    cursor.execute(
        """
        SELECT release, COUNT(*)
        FROM job_postings
        WHERE country_code = 'NG'
        GROUP BY release
        """
    )

    results = dict(cursor.fetchall())

    september_count = results["2026-09"]
    october_count = results["2026-10"]

    percentage_change = (
        (october_count - september_count) / september_count
    ) * 100

    assert abs(percentage_change) <= 20, (
        f"Nigeria changed by {percentage_change:.2f}%. "
        f"September: {september_count}, October: {october_count}"
    )