"""REST client handling, including teamtailorStream base class."""
import time

import requests
from pathlib import Path
from typing import Any, Dict, Optional, Iterable, Generator

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import APIKeyAuthenticator

from urllib.parse import urlparse, parse_qs

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class TeamtailorStream(RESTStream):
    """teamtailor stream class."""

    url_base = "https://api.teamtailor.com"
    records_jsonpath = "$.data[*]"  # Or override `parse_response`.
    next_page_token_jsonpath = "$.links.next"  # Or override `get_next_page_token`.
    includes = []
    extra_filters = {}

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Return a new authenticator object."""
        return APIKeyAuthenticator.create_for_stream(
            self,
            key="authorization",
            value=f"Token token={self.config.get('api_key')}",
            location="header"
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        if "api_version" in self.config:
            headers["x-api-version"] = self.config.get('api_version')
        return headers

    def get_next_page_token(
            self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""
        if self.next_page_token_jsonpath:
            all_matches = extract_jsonpath(
                self.next_page_token_jsonpath, response.json()
            )
            first_match = next(iter(all_matches), None)
            next_page_url = first_match
            parsed_url = urlparse(next_page_url)
            query_params = parse_qs(parsed_url.query)
            next_page_token = query_params.get('page[number]')
        else:
            next_page_token = response.headers.get("X-Next-Page", None)

        return next_page_token

    def get_url_params(
            self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}
        if next_page_token:
            params["page[number]"] = next_page_token
            params["page[size]"] = 30
        if self.replication_key:
            params["sort"] = "-updated-at"
        if self.includes:
            params["include"] = ",".join(self.includes)
        if self.extra_filters:
            for key, value in self.extra_filters.items():
                params[key] = value
        return params

    def prepare_request_payload(
            self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Optional[dict]:
        """Prepare the data payload for the REST API request.

        By default, no payload will be sent (return None).
        """
        # TODO: Delete this method if no payload is required. (Most REST APIs.)
        return None

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    def post_process(self, row: dict, context: Optional[dict]) -> dict:
        """As needed, append or transform raw data to match expected structure."""
        if self.replication_key == 'updated-at':
            row['updated-at'] = row['attributes']['updated-at']
        return row

    def backoff_wait_generator(self) -> Generator[int, None, None]:
        def _backoff_from_headers(retriable_api_error):
            response_headers = retriable_api_error.response.headers
            return int(response_headers.get("X-Rate-Limit-Reset", 0))

        return self.backoff_runtime(value=_backoff_from_headers)
