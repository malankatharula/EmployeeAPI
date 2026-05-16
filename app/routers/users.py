from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from passlib.context import CryptContext

router = APIRouter(prefix="/users", tags=["Users"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

@router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == user.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    existing = db.query(models.User).filter(models.User.employee_id == user.employee_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists for this employee")
    hashed = pwd_context.hash(user.password)
    new_user = models.User(
        employee_id=user.employee_id,
        hashed_password=hashed,
        is_admin=user.is_admin
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user