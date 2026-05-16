from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/", response_model=schemas.RoleOut, status_code=status.HTTP_201_CREATED)
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Role).filter(models.Role.name == role.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Role already exists")
    new_role = models.Role(**role.model_dump())
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

@router.get("/", response_model=list[schemas.RoleOut])
def get_roles(db: Session = Depends(get_db)):
    return db.query(models.Role).all()

@router.get("/{role_id}", response_model=schemas.RoleOut)
def get_role(role_id: UUID, db: Session = Depends(get_db)):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_id: UUID, db: Session = Depends(get_db)):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    db.delete(role)
    db.commit()