import pytest
import requests


def test_search_country_by_name(base_url, headers):
    response = requests.get(
        f"{base_url}/names.common/Kenya",
        headers=headers,
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()
    country = data["data"]["objects"][0]

    assert country["names"]["common"] == "Kenya"


@pytest.mark.parametrize(
    "code_type, code",
    [
        ("alpha_2", "KE"),
        ("alpha_3", "KEN"),
    ]
)
def test_search_country_by_code(base_url, headers, code_type, code):
    response = requests.get(
        f"{base_url}/codes.{code_type}/{code}",
        headers=headers,
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()
    country = data["data"]["objects"][0]

    assert country["codes"][code_type] == code
    assert country["names"]["common"] == "Kenya"


def test_search_country_by_currency(base_url, headers):
    response = requests.get(
        f"{base_url}/currencies/USD",
        headers=headers,
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()
    countries = data["data"]["objects"]

    assert len(countries) > 1

    for country in countries:
        currency_codes = [
            currency["code"]
            for currency in country["currencies"]
        ]

        assert "USD" in currency_codes


def test_search_countries_by_region(base_url, headers):
    response = requests.get(
        f"{base_url}/region/Africa",
        headers=headers,
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()
    countries = data["data"]["objects"]

    assert len(countries) > 0

    for country in countries:
        assert country["region"] == "Africa"


def test_nonexistent_country_returns_no_match(base_url, headers):
    response = requests.get(
        f"{base_url}/names.common/NotARealCountry",
        headers=headers,
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()
    countries = data["data"]["objects"]

    assert len(countries) == 0


def test_malformed_country_code_returns_no_match(base_url, headers):
    response = requests.get(
        f"{base_url}/codes.alpha_2/KENYA",
        headers=headers,
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()
    countries = data["data"]["objects"]

    assert len(countries) == 0


def test_empty_country_search_returns_not_found(base_url, headers):
    response = requests.get(
        f"{base_url}/names.common/",
        headers=headers,
        timeout=10
    )

    assert response.status_code == 404

    data = response.json()

    assert data["errors"][0]["code"] == "routeNotFound"


def test_country_name_with_accent_and_apostrophe(base_url, headers):
    response = requests.get(
        f"{base_url}/name",
        params={"q": "Côte d'Ivoire"},
        headers=headers,
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()
    countries = data["data"]["objects"]

    assert len(countries) > 0
    assert countries[0]["codes"]["alpha_2"] == "CI"


@pytest.mark.parametrize(
    "country_name",
    [
        "kenya",
        "KENYA",
        "Kenya",
    ]
)
def test_country_name_search_is_case_insensitive(
    base_url,
    headers,
    country_name
):
    response = requests.get(
        f"{base_url}/names.common/{country_name}",
        headers=headers,
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()
    countries = data["data"]["objects"]

    assert len(countries) > 0
    assert countries[0]["names"]["common"] == "Kenya"


@pytest.mark.parametrize(
    "search_name",
    [
        "Kenya",
        "Ken",
    ]
)
def test_full_and_partial_country_name_search(
    base_url,
    headers,
    search_name
):
    response = requests.get(
        f"{base_url}/name",
        params={"q": search_name},
        headers=headers,
        timeout=10
    )

    assert response.status_code == 200

    data = response.json()
    countries = data["data"]["objects"]

    assert len(countries) > 0

    country_codes = [
        country["codes"]["alpha_2"]
        for country in countries
    ]

    assert "KE" in country_codes


def test_two_letter_country_codes_are_unique(all_countries):
    codes = [
        country["codes"]["alpha_2"]
        for country in all_countries
        if country["codes"]["alpha_2"] != ""
    ]

    assert len(codes) == len(set(codes))
def test_country_population_is_not_negative(all_countries):
    for country in all_countries:
        assert country["population"] >= 0


def test_every_country_has_a_region(all_countries):
    for country in all_countries:
        assert country["region"] is not None
        assert country["region"] != ""