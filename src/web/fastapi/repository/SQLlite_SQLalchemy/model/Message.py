from email.policy import default
from typing import Optional

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Index
from datetime import datetime
import re

class Base(DeclarativeBase):
    pass


class Message_modern(Base):
    __tablename__ = "MessageFolder"
    
    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user:Mapped[str] = mapped_column(String(64), nullable=False, unique=False)
    user_id:Mapped[str] = mapped_column(String(9), unique=True, index=False)
    created_date:Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    updated_date:Mapped[datetime] = mapped_column(DateTime, nullable = True, default=None, onupdate=datetime.now())
    chain:Mapped[str] = mapped_column(String(255), nullable=False, unique=False)

    __table_args__ = (
        Index("idx_id_user_id", "user_id", "id"),
    )

    def __post_init__(self):
        self.__valid_user_id()


    def __valid_user_id(self):
        if not Dni_Nie_Validator.is_dni_nie_valid(self.user_id):
            raise ValueError("User ID must be a valid identification number")

class Message_classic(declarative_base()):
    __tablename__ = "MessageFolder"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String, nullable=False, unique=False)
    user_id = Column(String, unique=True, index=False)
    created_date = Column(DateTime, nullable=False, insert_default=datetime.now())
    updated_date = Column(DateTime, nullable = False, insert_default=datetime.now())
    chain = Column(String, nullable=False, unique=False)

    __table_args__ = (
        Index("idx_id_user_id", "user_id", "id"),
    )

    def __post_init__(self):
        self.__valid_user_id()


    def __valid_user_id(self):
        if not Dni_Nie_Validator.is_dni_nie_valid(self.user_id):
            raise ValueError("User ID must be a valid identification number")

class Dni_Nie_Validator:

    @staticmethod
    def is_dni_nie_valid(value) -> bool:
        DNI_NIE_PATTERN = re.compile(r'^(?:[0-9]{8}|[XYZ][0-9]{7})[A-Z]$')
        return bool(DNI_NIE_PATTERN.match(value))
    