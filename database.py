import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "dio-bank.db")

db = create_engine(
    f"sqlite:///{db_path}",
    connect_args={"check_same_thread": False}
)

Base = declarative_base()