from sqlalchemy import create_engine
from pydantic import PostgresDsn
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URI = PostgresDsn.build(
    scheme="postgresql",
    user="xgrowdb",
    password="D8mSNV7fhFvmSh3^$kND3rtDsRX!6rvHsyRXNSfmSJXY3MmtxQSTjiyY@ytFyJxQ",
    host="146.148.21.210",
    path=f"/{'xgrowdb' or ''}",
)
SQLALCHEMY_DATABASE_URL = 'sqlite:///./sql_lite.db'

def standard_connect():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})
    return engine




#engine = create_engine(
#    SQLALCHEMY_DATABASE_URI,
#    pool_pre_ping=True,
#)
