from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime
from uuid import UUID


class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleOut(RoleBase):
    id: UUID
    class Config:
        from_attributes = True


class DepartmentBase(BaseModel):
    name: str

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentOut(DepartmentBase):
    id: UUID
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    department_id: Optional[UUID] = None
    role_id: Optional[UUID] = None
    manager_id: Optional[UUID] = None
    hire_date: Optional[date] = None
    is_active: Optional[bool] = True

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    department_id: Optional[UUID] = None
    role_id: Optional[UUID] = None
    manager_id: Optional[UUID] = None
    hire_date: Optional[date] = None
    is_active: Optional[bool] = None

class EmployeeOut(EmployeeBase):
    id: UUID
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    employee_id: UUID
    password: str
    is_admin: Optional[bool] = False

class UserOut(BaseModel):
    id: UUID
    employee_id: UUID
    is_admin: bool
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    employee_id: Optional[str] = None