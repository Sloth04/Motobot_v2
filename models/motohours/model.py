from settings import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import INTEGER, CHAR, DATETIME

engine = create_engine(f'sqlite:///{cwd}/{DATABASE_NAME}')
Session = sessionmaker(bind=engine)

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    tg_user_id = Column(INTEGER, primary_key=True)
    user_nickname = Column(CHAR)
    user_lastname = Column(CHAR)
    children = relationship('Data')

    def __init__(self, tg_user_id: int, user_nickname: str, user_lastname: str):
        self.tg_user_id = tg_user_id
        self.user_nickname = user_nickname
        self.user_lastname = user_lastname

    def __repr__(self):
        info: str = f"Користувач [Ідентифікатор Telegram: {self.tg_user_id}," \
                    f"Им`я: {self.user_nickname}, Прізвище: {self.user_lastname}]"
        return info


class Data(Base):
    __tablename__ = 'motohours_data'

    id = Column(INTEGER, primary_key=True)
    tg_user_id = Column(INTEGER, ForeignKey('users.tg_user_id'))
    data = Column(INTEGER)
    received = Column(INTEGER)

    def __init__(self, tg_user_id: int, data: int, received: int):
        self.tg_user_id = tg_user_id
        self.data = data
        self.received = received

