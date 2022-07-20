from sqlalchemy import create_engine
from pydantic import PostgresDsn

SQLALCHEMY_DATABASE_URI = PostgresDsn.build(
    scheme="postgresql",
    user="xgrowdb",
    password="chuj",
    host="146.148.21.210",
    path=f"/{'xgrowdb' or ''}",
)


#engine = create_engine(
#    SQLALCHEMY_DATABASE_URI,
#    pool_pre_ping=True,
#)
