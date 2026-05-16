from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app import models, schemas
from app.auth import get_current_user, get_admin_user

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.post("/", response_model=schemas.EmployeeOut, status_code=status.HTTP_201_CREATED)
def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    existing = db.query(models.Employee).filter(models.Employee.email == employee.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_employee = models.Employee(**employee.model_dump())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

@router.get("/", response_model=list[schemas.EmployeeOut])
def get_employees(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Employee).all()

@router.get("/{employee_id}", response_model=schemas.EmployeeOut)
def get_employee(
    employee_id: UUID,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.patch("/{employee_id}", response_model=schemas.EmployeeOut)
def update_employee(
    employee_id: UUID,
    updates: schemas.EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(employee, field, value)
    db.commit()
    db.refresh(employee)
    return employee

@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: UUID,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user)
):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(employee)
    db.commit()