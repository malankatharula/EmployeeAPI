from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.post("/", response_model=schemas.DepartmentOut, status_code=status.HTTP_201_CREATED)
def create_department(dept: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Department).filter(models.Department.name == dept.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Department already exists")
    new_dept = models.Department(**dept.model_dump())
    db.add(new_dept)
    db.commit()
    db.refresh(new_dept)
    return new_dept

@router.get("/", response_model=list[schemas.DepartmentOut])
def get_departments(db: Session = Depends(get_db)):
    return db.query(models.Department).all()

@router.get("/{dept_id}", response_model=schemas.DepartmentOut)
def get_department(dept_id: UUID, db: Session = Depends(get_db)):
    dept = db.query(models.Department).filter(models.Department.id == dept_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept

@router.delete("/{dept_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(dept_id: UUID, db: Session = Depends(get_db)):
    dept = db.query(models.Department).filter(models.Department.id == dept_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    db.delete(dept)
    db.commit()