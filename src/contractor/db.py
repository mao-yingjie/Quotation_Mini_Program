
from contextlib import contextmanager
from sqlmodel import SQLModel, create_engine, Session
import os
from .utils.paths import DB_DEFAULT

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_DEFAULT}")
engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    from . import models  # ensure models are imported
    SQLModel.metadata.create_all(engine)

@contextmanager
def get_session():
    with Session(engine) as session:
        yield session
