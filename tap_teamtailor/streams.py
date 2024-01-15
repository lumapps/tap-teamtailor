"""Stream type classes for tap-teamtailor."""

from singer_sdk import typing as th

from tap_teamtailor.client import TeamtailorStream


def get_relationship_schema(includes: list[str]) -> th.Property:
    relationships_schema = th.Property("relationships", th.ObjectType(
        *[
            th.Property(
                include,
                th.ObjectType(
                    th.Property(
                        "data",
                        th.ObjectType(
                            th.Property(
                                "id",
                                th.StringType
                            ),
                            th.Property(
                                "type",
                                th.StringType
                            )
                        )
                    )
                )
            ) for include in includes
        ]
    ))
    return relationships_schema


class JobOffersStream(TeamtailorStream):
    """Define custom stream."""
    name = "job-offers"
    path = "/v1/job-offers"
    primary_keys = ["id"]
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"
    includes = ['job-application']
    extra_filters = {}

    schema = th.PropertiesList(
        th.Property("name", th.StringType),
        th.Property(
            "id",
            th.StringType,
            description="The job-offer system ID"
        ),
        th.Property(
            "attributes",
            th.ObjectType(
                th.Property("created-at", th.DateTimeType),
                th.Property("sent-at", th.DateTimeType),
                th.Property("answered-at", th.DateTimeType),
                th.Property("response", th.StringType),
                th.Property("status", th.StringType),
                th.Property("details", th.ObjectType(
                    th.Property('acceptance-message', th.StringType),
                    th.Property('rejection-message', th.StringType),
                    th.Property('salary', th.StringType),
                    th.Property('start-date', th.DateType)
                )),
            ),
            description="attributes of the job offer"
        ),
        get_relationship_schema(includes),
    ).to_dict()


class JobsStream(TeamtailorStream):
    """Define custom stream."""
    name = "jobs"
    path = "/v1/jobs"
    primary_keys = ["id"]
    replication_key = 'updated-at'
    includes = ['requisition']
    extra_filters = {"filter[status]": "all"}
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"
    schema = th.PropertiesList(
        th.Property(
            "id",
            th.StringType,
            description="The job system ID"
        ),
        th.Property("updated-at", th.DateTimeType),
        th.Property(
            "attributes",
            th.ObjectType(
                th.Property('apply-button-text', th.StringType),
                th.Property('body', th.StringType),
                th.Property('end-date', th.DateType),
                th.Property("human-status", th.StringType),
                th.Property("internal", th.BooleanType),
                th.Property("picture", th.StringType),
                th.Property("pinned", th.BooleanType),
                th.Property('start-date', th.DateType),
                th.Property('status', th.StringType),
                th.Property('tags', th.ArrayType(
                    th.StringType
                )),
                th.Property("title", th.StringType),
                th.Property("internal-name", th.StringType),
                th.Property("pitch", th.StringType),
                th.Property("external-application-url", th.StringType),
                th.Property("name-requirement", th.StringType),
                th.Property("resume-requirement", th.StringType),
                th.Property("cover-letter-requirement", th.StringType),
                th.Property("phone-requirement", th.StringType),
                th.Property("created-at", th.DateTimeType),
                th.Property("updated-at", th.DateTimeType),
                th.Property("sharing-image-layout", th.StringType),
                th.Property("mailbox", th.StringType),
                th.Property("remote-status", th.StringType),
            ),
            description="attributes of the job"
        ),
        get_relationship_schema(includes)
    ).to_dict()


class JobApplicationsStream(TeamtailorStream):
    """Define custom stream."""
    name = "job-applications"
    path = "/v1/job-applications"
    primary_keys = ["id"]
    replication_key = 'updated-at'
    includes = ['candidate', 'stage', 'job']
    extra_filters = {}
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"
    schema = th.PropertiesList(
        th.Property("name", th.StringType),
        th.Property("updated-at", th.DateTimeType),
        th.Property(
            "id",
            th.StringType,
            description="The job-application system ID"
        ),
        th.Property("updated-at", th.DateTimeType),
        th.Property(
            "attributes",
            th.ObjectType(
                th.Property('cover-letter', th.StringType),
                th.Property('created-at', th.DateTimeType),
                th.Property('referring-site', th.StringType),
                th.Property('referring-url', th.StringType),
                th.Property("rejected-at", th.DateTimeType),
                th.Property("sourced", th.BooleanType),
                th.Property("updated-at", th.DateTimeType),
                th.Property("row-order", th.IntegerType),
                th.Property("changed-stage-at", th.StringType),
            ),
            description="attributes of the job application"
        ),
        get_relationship_schema(includes),
    ).to_dict()


class StageStream(TeamtailorStream):
    """Define custom stream."""
    name = "stages"
    path = "/v1/stages"
    primary_keys = ["id"]
    replication_key = 'updated-at'
    includes = []
    extra_filters = {}

    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"
    schema = th.PropertiesList(
        th.Property(
            "id",
            th.StringType,
            description="The stage system ID"
        ),
        th.Property("updated-at", th.DateTimeType),
        th.Property(
            "attributes",
            th.ObjectType(
                th.Property('created-at', th.DateTimeType),
                th.Property('updated-at', th.DateTimeType),
                th.Property('name', th.StringType),
                th.Property("stage-type", th.StringType),
                th.Property("row-order", th.IntegerType),
                th.Property("active-job-applications-count", th.IntegerType),
                th.Property("rejected-job-applications-count", th.IntegerType),
            ),
            description="attributes of the stage"
        ),
        get_relationship_schema(includes),
    ).to_dict()


class RequisitionsStream(TeamtailorStream):
    """Define custom stream."""
    name = "requisitions"
    path = "/v1/requisitions"
    primary_keys = ["id"]
    includes = []
    extra_filters = {}
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"
    schema = th.PropertiesList(
        th.Property(
            "id",
            th.StringType,
            description="The requisition system ID"
        ),
        th.Property("updated-at", th.DateTimeType),
        th.Property(
            "attributes",
            th.ObjectType(
                th.Property('created-at', th.DateTimeType),
                th.Property('updated-at', th.DateTimeType),
                th.Property('job-title', th.StringType),
                th.Property("job-description", th.StringType),
                th.Property("country", th.StringType),
                th.Property("currency", th.StringType),
                th.Property("salary-time-unit", th.StringType),
                th.Property("min-salary", th.StringType),
                th.Property("max-salary", th.StringType),
                th.Property("status", th.StringType),
                th.Property("number-of-openings", th.IntegerType),
                th.Property("hired-count", th.IntegerType),
            ),
            description="attributes of the stage"
        ),
        get_relationship_schema(includes),
    ).to_dict()


class CandidatesStream(TeamtailorStream):
    """Define custom stream."""
    name = "candidates"
    path = "/v1/candidates"
    primary_keys = ["id"]
    includes = []
    extra_filters = {}
    replication_key = 'updated-at'

    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"
    schema = th.PropertiesList(
        th.Property(
            "id",
            th.StringType,
            description="The candidate system ID"
        ),
        th.Property("updated-at", th.DateTimeType),
        th.Property(
            "attributes",
            th.ObjectType(
                th.Property('connected', th.BooleanType),
                th.Property('created-at', th.DateTimeType),
                th.Property('email', th.EmailType),
                th.Property("facebook-id", th.StringType),
                th.Property("first-name", th.StringType),
                th.Property("internal", th.BooleanType),
                th.Property("last-name", th.StringType),
                th.Property("linkedin-uid", th.StringType),
                th.Property("linkedin-url", th.StringType),
                th.Property("original-resume", th.StringType),
                th.Property("phone", th.StringType),
                th.Property("picture", th.StringType),
                th.Property('pitch', th.StringType),
                th.Property('referring-site', th.StringType),
                th.Property('referring-url', th.StringType),
                th.Property("referred", th.BooleanType),
                th.Property("resume", th.StringType),
                th.Property("sourced", th.BooleanType),
                th.Property("unsubscribed", th.BooleanType),
                th.Property("updated-at", th.DateTimeType),
                th.Property("facebook-profile", th.StringType),
                th.Property("linkedin-profile", th.StringType),
                th.Property("tags", th.ArrayType(th.StringType)),
            ),
            description="attributes of the candidate"
        ),
        get_relationship_schema(includes),
    ).to_dict()
