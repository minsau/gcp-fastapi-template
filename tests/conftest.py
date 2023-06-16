import random
import string
from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlmodel import SQLModel

# from app.core.base_class import Base
from app.core.config import settings
from app.core.session import SessionLocal, engine, get_db
from app.models import Vehicle
from app.models.user import User
from app.providers import vehicle as vehicle_providers
from app.providers.user import user as user_provider
from app.schemas.user import UserCreate
from app.schemas.vehicle import VehicleCreate
from main import app
from tests.factories import TicketFactory, UserFactory, VehicleFactory
from tests.utils.auth import get_superuser_token_headers
from tests.utils.user import authentication_token_from_email


@pytest.fixture()
def connection():
    with engine.begin() as conn:
        SQLModel.metadata.bind = conn
        SQLModel.metadata.create_all()
        yield conn
        # conn.rollback()
        SQLModel.metadata.drop_all()


@pytest.fixture(autouse=True)
def db(connection):
    SessionLocal.configure(bind=connection)
    with SessionLocal() as _session:
        UserFactory._meta.sqlalchemy_session = _session
        VehicleFactory._meta.sqlalchemy_session = _session
        TicketFactory._meta.sqlalchemy_session = _session
        yield _session


@pytest.fixture(autouse=True)
def override_dependency(db: Session) -> None:
    app.dependency_overrides[get_db] = lambda: db


@pytest.fixture()
def client() -> Generator:
    with TestClient(app) as c:
        yield c


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


@pytest.fixture()
def random_user(db: Session) -> User:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(username=email, email=email, password=password, is_superuser=False)
    user = user_provider.create(db=db, obj_in=user_in)
    return user


@pytest.fixture()
def user_with_pass(db: Session) -> User:
    def _user_with_pass(password: str) -> User:
        email = random_email()
        user_in = UserCreate(username=email, email=email, password=password, is_superuser=True)
        user = user_provider.create(db=db, obj_in=user_in)
        return user

    return _user_with_pass


@pytest.fixture()
def superuser_token_headers(client: TestClient, user_with_pass) -> Dict[str, str]:
    password = random_lower_string()
    user = user_with_pass(password)
    return get_superuser_token_headers(client, user=user, password=password)


@pytest.fixture()
def normal_user_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    return authentication_token_from_email(client=client, email=settings.EMAIL_TEST_USER, db=db)


@pytest.fixture()
def random_vehicle(db: Session, random_user: User) -> Vehicle:
    vehicle = VehicleFactory.create(user_id=random_user.id)
    db.commit()
    return vehicle


@pytest.fixture()
def create_batch_of_vehicles(db: Session, random_user: User) -> None:
    def __create_batch_of_vehicles(size: int):
        created_vehicles = []
        for _ in range(size):
            vehicle = VehicleFactory.build(user_id=random_user.id)
            vehicle_created = vehicle_providers.create_vehicle_by_user_id(
                db=db,
                user_id=random_user.id,
                vehicle=VehicleCreate(
                    niv=vehicle.niv,
                    plate=vehicle.plate,
                ),
            )

            created_vehicles.append(vehicle_created)

        return created_vehicles

    return __create_batch_of_vehicles
