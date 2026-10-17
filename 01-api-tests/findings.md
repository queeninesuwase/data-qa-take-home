# API Findings

## Non-existent country search

When I searched for a country that does not exist, the API returned HTTP 200 instead of 404.

The response contained an empty `objects` list and a total count of 0.

I expected a not-found status such as 404, but the API treats the request as successful and represents "no result" using an empty response.

This matters because a client should not rely only on the HTTP status code to decide whether a country was found. It should also check the returned data.

## Malformed country code

I also tested an invalid two-letter country code using `KENYA`.

The API returned HTTP 200 with an empty `objects` list instead of an error status.

This means invalid searches and malformed codes are both represented as successful requests with no matching data, so a client should check the response body as well as the status code.

## Empty country search

An empty country search returned HTTP 404 with the error code `routeNotFound`.

This is different from a non-existent country name or malformed country code, which returned HTTP 200 with an empty result.

This difference matters because clients need to handle these invalid-input cases differently.

## Country name with special characters

Searching for `Côte d'Ivoire` using the exact common-name endpoint returned no results.

I found that the API stores the common name as `Ivory Coast`, while `Côte d'Ivoire` appears in its native and official names.

Using the broader name search returned the correct country.

This matters because users may search using different valid names for the same country, so an exact common-name lookup may not always be enough.

## Missing two-letter country codes

While checking whether two-letter country codes were unique, I found 4 records with an empty `alpha_2` value:

- Abkhazia
- NorthernCyprus
- Somaliland
- South Ossetia

The non-empty country codes were unique.

This matters because a client that expects every country record to have an ISO two-letter code may need to handle these records separately.

## API version change

The task brief refers to an older REST Countries API that did not require an API key.

When I tested the old endpoint, it redirected to a legacy data file. I checked the current API and used the maintained v5 version instead.

The current version requires authentication, so I stored the API key in an environment variable.