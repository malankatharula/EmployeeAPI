import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app import models
from app.auth import hash_password

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def admin_token(client):
    db = TestingSessionLocal()
    employee = models.Employee(
        first_name="Test",
        last_name="Admin",
        email="testadmin@company.com",
        is_active=True
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)

    user = models.User(
        employee_id=employee.id,
        hashed_password=hash_password("testpass123"),
        is_admin=True
    )
    db.add(user)
    db.commit()
    db.close()

    response = client.post("/auth/login", data={
        "username": "testadmin@company.com",
        "password": "testpass123"
    })
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_role(client, auth_headers):
    response = client.post("/roles/", json={
        "name": "Engineer",
        "description": "Software Engineer"
    }, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["name"] == "Engineer"


def test_create_duplicate_role(client, auth_headers):
    client.post("/roles/", json={"name": "Engineer"}, headers=auth_headers)
    response = client.post("/roles/", json={"name": "Engineer"}, headers=auth_headers)
    assert response.status_code == 400


def test_get_roles(client, auth_headers):
    client.post("/roles/", json={"name": "Engineer"}, headers=auth_headers)
    response = client.get("/roles/")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_create_department(client, auth_headers):
    response = client.post("/departments/", json={"name": "Engineering"})
    assert response.status_code == 201
    assert response.json()["name"] == "Engineering"


def test_create_employee_requires_admin(client):
    response = client.post("/employees/", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@company.com"
    })
    assert response.status_code == 401


def test_create_employee(client, auth_headers):
    response = client.post("/employees/", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@company.com",
        "is_active": True
    }, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["email"] == "john@company.com"


def test_get_employees_requires_auth(client):
    response = client.get("/employees/")
    assert response.status_code == 401


def test_get_employees(client, auth_headers):
    response = client.get("/employees/", headers=auth_headers)
    assert response.status_code == 200


def test_login_wrong_password(client, auth_headers):
    response = client.post("/auth/login", data={
        "username": "testadmin@company.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401