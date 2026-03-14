import sqlite3
from ..data.queries import Queries
from .model.Message import Message
from typing import Optional
from datetime import datetime
from pathlib import Path

class Repository:

    def __init__(self, database_path: str):
        self.__base_dir = Path(__file__).parent
        self.__conn = sqlite3.connect(database=self.__base_dir / database_path, check_same_thread=False)
        self.__create_table()

    def __create_table(self):
        self.__conn.execute(Queries.CREATE_MESSAGE_TABLE)
        self.__conn.commit()

    def save(self, message: Message) -> Message:
        cursor = self.__conn.execute(Queries.ADD_MESSAGE, (message.user, message.user_id, message.updated_date, message.chain))
        self.__conn.commit()
        message.id = cursor.lastrowid
    
        return message

    def find_by_id(self, id: int) -> Optional[Message]:
        #row is a dictionary. Access each element by its id
        row = self.__conn.execute(Queries.GET_BY_ID, (id,)).fetchone()
        return Message(id = row[0], user = row[1], user_id = row[2], created_date=datetime.fromisoformat(row[3]), 
                       updated_date=datetime.fromisoformat(row[4]), chain = row[5]) if row else None

    def get_all(self) -> list[Message]:
        rows = self.__conn.execute(Queries.GET_ALL_ORDERED).fetchall()
        return [Message(id = r[0], user = r[1], user_id = r[2], created_date=datetime.fromisoformat(r[3]), 
                       updated_date=datetime.fromisoformat(r[4]), chain = r[5]) for r in rows]

    def update(self, message: Message) -> None:
        self.__conn.execute(Queries.UPDATE, (message.chain, message.user_id))
        self.__conn.commit()

    def remove(self, id: int) -> None:
        self.__conn.execute(Queries.DELETED_BY_ID, (id,))
        self.__conn.commit()

    def close_connmection(self):
        self.__conn.close()