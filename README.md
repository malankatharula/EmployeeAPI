# Employee Management API

A production-grade REST API built with FastAPI, PostgreSQL, and Docker. Demonstrates backend engineering fundamentals including database migrations, JWT authentication, role-based access control, and automated testing.

## Tech Stack

- **FastAPI** — async REST API framework
- **PostgreSQL** — relational database
- **SQLAlchemy** — ORM for database interaction
- **Alembic** — database schema migrations
- **JWT (python-jose)** — stateless authentication
- **bcrypt (passlib)** — password hashing
- **Docker + Docker Compose** — containerised multi-service setup
- **Pytest** — automated API testing

## Features

- Full CRUD for Employees, Departments, and Roles
- JWT login with Bearer token authentication
- Role-based access control — admin vs regular user
- Database migrations with version control via Alembic
- 10 automated tests covering auth, CRUD, and access control
- Auto-generated Swagger UI at `/docs`

## Data Model

- **Employees** — belong to departments, have roles, report to managers (self-referential)
- **Departments** — contain employees, have a designated manager
- **Roles** — assigned to employees (Software Engineer, HR Manager, etc.)
- **Users** — linked to employees, store hashed passwords and admin status

## Getting Started

### Prerequisites
- Docker Desktop

### Run locally

```bash
git clone https://github.com/malankatharula/EmployeeAPI.git
cd EmployeeAPI
cp .env.example .env
docker compose up --build
```

API runs at `http://localhost:8000`  
Swagger UI at `http://localhost:8000/docs`

### Environment variables

Create a `.env` file with:

POSTGRES_USER=admin
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=employeedb
SECRET_KEY=your-secret-key

### Run database migrations

```bash
docker compose exec api alembic upgrade head
```

### Run tests

```bash
docker compose exec api pytest tests/ -v
```

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/login` | None | Get JWT token |
| GET | `/employees/` | User | List all employees |
| POST | `/employees/` | Admin | Create employee |
| PATCH | `/employees/{id}` | Admin | Update employee |
| DELETE | `/employees/{id}` | Admin | Delete employee |
| GET | `/departments/` | None | List departments |
| POST | `/departments/` | None | Create department |
| GET | `/roles/` | None | List roles |
| POST | `/roles/` | None | Create role |
| GET | `/health` | None | Health check |

## Author

Malanka Tharula — [GitHub](https://github.com/malankatharula) · [LinkedIn](https://linkedin.com/in/malanka-tharula-b329432a7)