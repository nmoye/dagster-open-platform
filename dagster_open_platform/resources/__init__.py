import os

from dagster import EnvVar, file_relative_path
from dagster_cloud.dagster_insights import InsightsBigQueryResource
from dagster_dbt import DbtCliResource
from dagster_embedded_elt.sling.resources import (
    SlingConnectionResource,
    SlingResource,
)
from dagster_slack import SlackResource
from dagster_snowflake import SnowflakeResource

from ..utils.environment_helpers import get_dbt_target, get_environment, get_schema_for_environment
from .hightouch_resource import ConfigurableHightouchResource
from .scoutos_resource import GithubResource, ScoutosResource
from .sling_resource import CustomSlingResource, SlingPostgresConfig, SlingSnowflakeConfig

embedded_elt_resource = SlingResource(
    connections=[
        SlingConnectionResource(
            name="CLOUD_PRODUCTION",
            type="postgres",
            host=EnvVar("CLOUD_PROD_READ_REPLICA_POSTGRES_HOST"),  # type: ignore
            user=EnvVar("CLOUD_PROD_POSTGRES_USER"),  # type: ignore
            database="dagster",  # type: ignore
            password=EnvVar("CLOUD_PROD_POSTGRES_PASSWORD"),  # type: ignore
            ssl_mode="require",  # type: ignore
            ssh_tunnel=EnvVar("CLOUD_PROD_BASTION_URI"),  # type: ignore
            ssh_private_key=EnvVar("POSTGRES_SSH_PRIVATE_KEY"),  # type: ignore
        ),
        SlingConnectionResource(
            name="SLING_DB",
            type="snowflake",
            host=EnvVar("SNOWFLAKE_ACCOUNT"),  # type: ignore
            user=EnvVar("SNOWFLAKE_SLING_USER"),  # type: ignore
            password=EnvVar("SNOWFLAKE_SLING_PASSWORD"),  # type: ignore
            database="sandbox" if get_environment() != "PROD" else "sling",  # type: ignore
            schema=get_schema_for_environment("cloud_product"),  # type: ignore
            warehouse="sling",  # type: ignore
            role="purina" if get_environment() != "PROD" else "sling",  # type: ignore
        ),
    ]
)

DBT_MANIFEST_PATH = file_relative_path(
    __file__, "../../dagster_open_platform_dbt/target/manifest.json"
)

bigquery_resource = InsightsBigQueryResource(
    gcp_credentials=EnvVar("GCP_CREDENTIALS"),
)

snowflake_resource = SnowflakeResource(
    user=EnvVar("SNOWFLAKE_USER"),
    account=EnvVar("SNOWFLAKE_ACCOUNT"),
    password=EnvVar("SNOWFLAKE_PASSWORD"),
    role=os.getenv("SNOWFLAKE_ROLE", "PURINA"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE", "PURINA"),
)

dbt_resource = DbtCliResource(
    project_dir=file_relative_path(__file__, "../../dagster_open_platform_dbt"),
    profiles_dir=file_relative_path(__file__, "../../dagster_open_platform_dbt"),
    target=get_dbt_target(),
)

slack_resource = SlackResource(token=EnvVar("SLACK_ANALYTICS_TOKEN"))

cloud_prod_reporting_sling_resource = CustomSlingResource(
    postgres_config=SlingPostgresConfig(
        host=EnvVar("CLOUD_PROD_REPORTING_POSTGRES_HOST"),
        user=EnvVar("CLOUD_PROD_POSTGRES_USER"),
        database="dagster",
        password=EnvVar("CLOUD_PROD_REPORTING_POSTGRES_PASSWORD"),
        ssh_tunnel=EnvVar("CLOUD_PROD_BASTION_URI"),
        ssh_private_key=EnvVar("POSTGRES_SSH_PRIVATE_KEY"),
    ),
    snowflake_config=SlingSnowflakeConfig(
        host=EnvVar("SNOWFLAKE_PURINA_ACCOUNT"),
        user=EnvVar("SNOWFLAKE_PURINA_USER"),
        password=EnvVar("SNOWFLAKE_PURINA_PASSWORD"),
        database="purina",
        warehouse="purina",
        role="purina",
    ),
)

cloud_prod_read_replica_sling_resource = CustomSlingResource(
    postgres_config=SlingPostgresConfig(
        host=EnvVar("CLOUD_PROD_READ_REPLICA_POSTGRES_HOST"),
        user=EnvVar("CLOUD_PROD_POSTGRES_USER"),
        database="dagster",
        password=EnvVar("CLOUD_PROD_POSTGRES_PASSWORD"),
        ssh_tunnel=EnvVar("CLOUD_PROD_BASTION_URI"),
        ssh_private_key=EnvVar("POSTGRES_SSH_PRIVATE_KEY"),
    ),
    snowflake_config=SlingSnowflakeConfig(
        host=EnvVar("SNOWFLAKE_PURINA_ACCOUNT"),
        user=EnvVar("SNOWFLAKE_PURINA_USER"),
        password=EnvVar("SNOWFLAKE_PURINA_PASSWORD"),
        database="purina",
        warehouse="purina",
        role="purina",
    ),
)

cloud_prod_sling_resource = CustomSlingResource(
    postgres_config=SlingPostgresConfig(
        host=EnvVar("CLOUD_PROD_POSTGRES_HOST"),
        user=EnvVar("CLOUD_PROD_POSTGRES_USER"),
        database="dagster",
        password=EnvVar("CLOUD_PROD_POSTGRES_PASSWORD"),
        ssh_tunnel=EnvVar("CLOUD_PROD_BASTION_URI"),
        ssh_private_key=EnvVar("POSTGRES_SSH_PRIVATE_KEY"),
    ),
    snowflake_config=SlingSnowflakeConfig(
        host=EnvVar("SNOWFLAKE_PURINA_ACCOUNT"),
        user=EnvVar("SNOWFLAKE_PURINA_USER"),
        password=EnvVar("SNOWFLAKE_PURINA_PASSWORD"),
        database="purina",
        warehouse="purina",
        role="purina",
    ),
)


github_resource = GithubResource(github_token=EnvVar("GITHUB_TOKEN"))
scoutos_resource = ScoutosResource(api_key=EnvVar("SCOUTOS_API_KEY"))
hightouch_resource = ConfigurableHightouchResource(api_key=EnvVar("HIGHTOUCH_API_KEY"))
