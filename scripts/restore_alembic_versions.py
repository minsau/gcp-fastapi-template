import logging

from sqlmodel import Session

from app.core.init_db import restore_alembic_versions
from app.core.session import engine

logger = logging.getLogger(__name__)


def init() -> None:
    db = Session(engine)
    restore_alembic_versions(db)


def main() -> None:
    
    logger.info("Restoring alembic versions")
    init()
    logger.info("Versions restored")


if __name__ == "__main__":
    main()
