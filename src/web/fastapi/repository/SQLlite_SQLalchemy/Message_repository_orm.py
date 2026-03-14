from datetime import datetime
from http.client import BAD_REQUEST
from logging import Logger

from fastapi import HTTPException
from requests import delete
from sqlalchemy import create_engine, exists, select
from sqlalchemy.orm import sessionmaker

from .model.Message import Message_modern, Message_classic, Base
from typing import Optional
from pathlib import Path

class Repository:

    logger = Logger(name = "repository_orm")

    def __init__(self, database_path: str):
        self.__base_dir = Path(__file__).parent
        self.__engine = create_engine(f"sqlite:///{self.__base_dir / database_path}", 
                                    connect_args={"check_same_thread": False}, 
                                    hide_parameters=True,
                                    logging_name="SqlAlchemyRepo")
        self.__session = sessionmaker(bind=self.__engine, autocommit=False, autoflush=False)
        self.__create_tables()

    def __create_tables(self):
        Base.metadata.create_all(self.__engine)

    def save(self, message: Message_modern) -> Message_modern:
        db = self.__session()
        rows = db.query(Message_modern).filter_by(user_id = message.user_id).count()
        if rows == 1:
            raise HTTPException(BAD_REQUEST, detail = "User with id already exists")
        else:
           db.add(message)
           db.commit()
           db.refresh(message)
           db.close()

        return message

    def find_by_id(self, id: int) -> Optional[Message_modern]:
        #row is a dictionary. Access each element by its id
        db = self.__session()
        row = db.query(Message_modern).filter_by(id = id).one_or_none()
        if row is not None:
            raise HTTPException(status_code=400, detail= f"Message with ID {id} not found")
        
        db.close()
        return row
    
    def get_all(self) -> list[Message_modern]:
        db = self.__session()
        query = db.query(Message_modern)
        if query.count() < 1:
            return list()
        
        all_messages = query.all()
        db.close()

        return all_messages
        
    def update(self, userId: str, user: str) -> None:
        db = self.__session()

        exists_row = db.scalar(
            select(exists().where(Message_modern.user_id == userId, Message_modern.user == user))
        )
        
        if not exists_row:
            raise HTTPException(status_code= 400, detail = f"User {user} with ID {userId} message not found")
        
        db.query(Message_modern).filter(Message_modern.user == user, Message_modern.user_id == userId).update(
            values = {"chain": "las queries ya no fallan", "user": "Peperoni"}, 
                              synchronize_session="evaluate")
        db.commit()
        db.close()

    def remove(self, id: int) -> None:
        optional_row = self.find_by_id(id)
        if optional_row is None:
            raise HTTPException(status_code= 400, detail = f"Message with ID {id} not found")
        
        db = self.__session()
        db.query(Message_modern).filter(Message_modern.id == id).delete(synchronize_session="evaluate")
    
    def remove_all(self) -> None:
        db = self.__session()

        exists_any = db.scalar(
            select(exists().select_from(Message_modern))
        )
        if not exists_any:
            raise HTTPException(status_code= 400, detail = f"There is not messages registered")
        
        db.query(Message_modern).delete(synchronize_session=False)
        db.commit()
        db.close()