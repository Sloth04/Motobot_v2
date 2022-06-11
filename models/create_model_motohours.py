from models.motohours.model import Base, engine


def create_db():
    Base.metadata.create_all(engine)
