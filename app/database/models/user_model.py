from datetime import date
from enum import Enum
from typing import Optional, List, Dict, Any
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class UserRole(str, Enum):
    ADMIN = "admin"
    HR = "hr"
    USER = "user"

class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    name = Column(String, nullable=True)
    hire_date = Column(Date, nullable=True)
    birth_date = Column(Date, nullable=True)
    work_experience = Column(Integer, nullable=True)
    position = Column(String, nullable=True)
    department = Column(String, nullable=True)  
    role = Column(String, default=UserRole.USER.value)
    is_active = Column(Boolean, default=True)
    t_points = Column(Integer, default=0)  
    
    def to_entity(self) -> 'User':
        """Convert ORM model to domain entity"""
        return User(
            id=self.id,
            telegram_id=self.telegram_id,
            username=self.username,
            name=self.name,
            hire_date=self.hire_date,
            birth_date=self.birth_date,
            work_experience=self.work_experience,
            position=self.position,
            department=self.department,  
            role=UserRole(self.role),
            is_active=self.is_active,
            t_points=self.t_points  
        )

class User:
    def __init__(
        self,
        id: Optional[int] = None,
        telegram_id: int = None,
        username: Optional[str] = None,
        name: Optional[str] = None,
        hire_date: Optional[date] = None,
        birth_date: Optional[date] = None,
        work_experience: Optional[int] = None,
        position: Optional[str] = None,
        department: Optional[str] = None,  
        role: UserRole = UserRole.USER,
        is_active: bool = True,
        t_points: int = 0  
    ):
        self.id = id
        self.telegram_id = telegram_id
        self.username = username
        self.name = name
        self.hire_date = hire_date
        self.birth_date = birth_date
        self.work_experience = work_experience
        self.position = position
        self.department = department  
        self.role = role
        self.is_active = is_active
        self.t_points = t_points  
        
    def to_model(self) -> UserModel:
        """Convert domain entity to ORM model"""
        return UserModel(
            id=self.id,
            telegram_id=self.telegram_id,
            username=self.username,
            name=self.name,
            hire_date=self.hire_date,
            birth_date=self.birth_date,
            work_experience=self.work_experience,
            position=self.position,
            department=self.department, 
            role=self.role.value,
            is_active=self.is_active,
            t_points=self.t_points  
        )
    
    def can_manage_users(self) -> bool:
        """Проверяет, может ли пользователь управлять другими пользователями"""
        return self.role in [UserRole.ADMIN, UserRole.HR] and self.is_active