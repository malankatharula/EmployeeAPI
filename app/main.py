from fastapi import FastAPI
from app.routers import roles, departments, employees, users, auth

app = FastAPI(
    title="Employee Management API",
    description="Production-grade REST API with PostgreSQL and JWT auth",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(roles.router)
app.include_router(departments.router)
app.include_router(employees.router)
app.include_router(users.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}