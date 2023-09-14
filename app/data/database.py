from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app import settings
from app.data.postgresSQLconnection.connect_connector import connect_with_connector
from app.data.postgresSQLconnection.standard import standard_connect

#if settings.DEVELOPER_MODE:
#SessionLocal = sessionmaker(bind=standard_connect(), autocommit=False, autoflush=False, )
#else:
SessionLocal = sessionmaker(bind=connect_with_connector(), autocommit=False, autoflush=False, )
''' 
    for deploy plz use connect_with_connector() in bind Sessionmaker,
    for localhost use: standard_connect()
'''
Base = declarative_base()


def getDataBase():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#https://github.com/GoogleCloudPlatform/python-docs-samples/tree/7fb9175993fd3bb0511ca1bdb0612d8768f9a0a3/cloud-sql/postgres/sqlalchemy