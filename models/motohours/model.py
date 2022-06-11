from settings import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


engine = create_engine(f'sqlite:///{cwd}/{DATABASE_NAME}')
Session = sessionmaker(bind=engine)

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    tg_user_id = Column(Integer, primary_key=True)
    user_nickname = Column(String)
    user_lastname = Column(String)
    children = relationship('Data')

    def __init__(self, tg_user_id: int, user_nickname: str, user_lastname: str):
        self.tg_user_id = tg_user_id
        self.user_nickname = user_nickname
        self.user_lastname = user_lastname

    def __repr__(self):
        info: str = f'Пользователь [Идентификатор Tg: {self.tg_user_id},' \
                    f'Имя: {self.user_nickname}, Фамилия: {self.user_lastname}]'
        return info

    class Data(Base):
        __tablename__ = 'motohours_data'

        id = Column(Integer, primary_key=True)
        tg_user = Column(Integer, ForeignKey('users.tg_user_id'))
        data = Column(Integer)
        received = Column(String)

        def __init__(self, tg_id: int, data: int, received: str):
            self.tg_id = tg_id
            self.data = data
            self.received = received

