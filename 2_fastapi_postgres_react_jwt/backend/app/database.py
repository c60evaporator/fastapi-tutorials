from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

from create_postgres_db import check_and_create_postgres_db

# DBのURLをSQLAlchemy形式で記載
DB_NAME = os.environ['DB_NAME']
POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
DB_HOST = os.environ['DB_HOST']
SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
# 該当DBがなければ作成 (PostgreSQLのみ)
check_and_create_postgres_db(DB_NAME, POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, 5432)
# SQLAlchemyのengineを作成
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# DBとのセッション確立用インスタンスを作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Baseクラスを作成 (後ほどSQLAlchemyのスキーマ作成に使用)
Base = declarative_base()