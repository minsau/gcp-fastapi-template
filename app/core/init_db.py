import logging

from sqlalchemy import MetaData
from sqlalchemy.orm import Session

from app.core import base  # noqa: F401
from app.core.config import settings
from app.providers.user import user as user_provider
from app.schemas.user import UserCreate

logger = logging.getLogger(__name__)


def restore_alembic_versions(db: Session):
    # Load the metadata
    metadata = MetaData()
    metadata.reflect(bind=db.bind)

    # Get the alembic_version table
    alembic_version = metadata.tables.get("alembic_version")

    # Check if the table exists
    if alembic_version is not None:
        # Delete all rows from the alembic_version table
        delete_query = alembic_version.delete()
        db.execute(delete_query)
        db.commit()
        logger.info("All rows deleted from the alembic_version table.")
    else:
        logger.info("The alembic_version table does not exist.")


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = user_provider.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = user_provider.create(db, obj_in=user_in)  # noqa: F841
