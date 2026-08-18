from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

load_dotenv()

DATABASE_URL = (
    f"mysql+pymysql://"
    f"{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASS')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

engine = create_engine(
    DATABASE_URL,

    pool_pre_ping=True,

    pool_recycle=3600,

    echo=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)