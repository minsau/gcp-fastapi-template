import json
import os
import secrets
from typing import Any, Dict, List, Optional, Union

from google.cloud import secretmanager
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator


def gcp_secret_manager_settings_source(settings: BaseSettings) -> dict[str, Any]:
    if not os.getenv("USE_GCP", "False").lower() == "true":
        return {}

    GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
    GCP_SECRET_ID = os.getenv("GCP_SECRET_ID")
    client = secretmanager.SecretManagerServiceClient()
    project_id = GCP_PROJECT_ID
    secret_version_path = f"projects/{project_id}/secrets/{GCP_SECRET_ID}/versions/latest"
    response = client.access_secret_version(request={"name": secret_version_path})
    secret_value = response.payload.data.decode("UTF-8")
    return json.loads(secret_value)


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    USE_GCP: bool = False
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str = "localhost"
    SERVER_HOST: AnyHttpUrl = "http://localhost"
    SELENIUM_HOST: AnyHttpUrl = "http://localhost:4444/wd/hub"
    BACKEND_CORS_ORIGINS: Optional[list[AnyHttpUrl]] = []

    GCP_PROJECT_ID: str = "my_project_id"
    GCP_REGION: str = "us-central1"
    GCP_INSTANCE_NAME: str = "my_instance_name"
    GCP_DB_NAME: str = "my_db_name"
    GCP_DB_USER: str = "my_db_user"
    GCP_DB_PASS: str = "my_db_pass"
    PRIVATE_IP: bool = False
    GCP_SECRET_ID: str = "my-secret-id"
    GCP_HIGH_PRIORITY_QUEUE_ID: str
    USE_CLOUD_TASKS: bool

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Optional[list[AnyHttpUrl]]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "my_project_name"
    ENVIRONMENT: str = "development"
    SENTRY_DSN: Optional[HttpUrl] = None

    # @validator("SENTRY_DSN", pre=True)
    # def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
    #     if len(v) == 0:
    #         return None
    #     return v

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "test"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "/app/app/email-templates/build"
    EMAILS_ENABLED: bool = False

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST") and values.get("SMTP_PORT") and values.get("EMAILS_FROM_EMAIL")
        )

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str
    USERS_OPEN_REGISTRATION: bool = False

    class Config:
        case_sensitive = True

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                init_settings,
                env_settings,
                gcp_secret_manager_settings_source,
                file_secret_settings,
            )


settings = Settings()
