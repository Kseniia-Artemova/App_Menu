from fastapi import FastAPI
from sqlalchemy import create_engine
from database import SessionLocal

app = FastAPI()

db = SessionLocal()
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
