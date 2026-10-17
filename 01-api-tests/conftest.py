import os

import pytest
import requests


@pytest.fixture(scope="session")
def base_url():
    return "https://api.restcountries.com/countries/v5"


@pytest.fixture(scope="session")
def headers():
    api_key = os.getenv("REST_COUNTRIES_API_KEY")

    if not api_key:
        pytest.fail("REST_COUNTRIES_API_KEY is not set")

    return {
        "Authorization": f"Bearer {api_key}"
    }


@pytest.fixture(scope="session")
def all_countries(base_url, headers):
    countries = []
    offset = 0

    while True:
        response = requests.get(
            base_url,
            headers=headers,
            params={
                "limit": 100,
                "offset": offset
            },
            timeout=10
        )

        assert response.status_code == 200

        data = response.json()["data"]
        batch = data["objects"]

        countries.extend(batch)

        if not data["meta"]["more"]:
            break

        offset += len(batch)

    return countries