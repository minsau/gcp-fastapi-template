from typing import Generator

import pg8000
from google.cloud.sql.connector import Connector, IPTypes
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

ip_type = IPTypes.PRIVATE if settings.PRIVATE_IP else IPTypes.PUBLIC
connector = Connector()


def getconn() -> pg8000.dbapi.Connection:
    instance_connection_name = settings.GCP_INSTANCE_NAME
    db_user = settings.GCP_DB_USER
    db_name = settings.GCP_DB_NAME
    db_pass = settings.GCP_DB_PASS

    conn: pg8000.dbapi.Connection = connector.connect(
        instance_connection_name,
        "pg8000",
        user=db_user,
        password=db_pass,
        db=db_name,
        ip_type=ip_type,
    )
    return conn


if settings.USE_GCP:
    engine = create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=2,
    )
else:
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
