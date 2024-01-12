"""teamtailor tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers
from tap_teamtailor.streams import (
    JobOffersStream,
    JobApplicationsStream,
    StageStream, JobsStream,
    RequisitionsStream, CandidatesStream
)

STREAM_TYPES = [
    JobOffersStream,
    JobApplicationsStream,
    StageStream,
    JobsStream,
    RequisitionsStream,
    CandidatesStream
]


class Tapteamtailor(Tap):
    """teamtailor tap class."""
    name = "tap-teamtailor"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType,
            required=True,
            description="The api key to authorize against the API service"
        ),
        th.Property(
            "api_url",
            th.StringType,
            default="https://api.teamtailor.com",
            description="The base url for the API service"
        ),
        th.Property(
            "api_version",
            th.StringType,
            default="20231215",
            description="The api version for the API service"
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]


if __name__ == "__main__":
    Tapteamtailor.cli()
