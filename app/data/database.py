from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.data.postgresSQLconnection.connect_auto_iam_auth import connect_with_connector_auto_iam_authn
from app.data.postgresSQLconnection.connect_connector import connect_with_connector #<==
from app.data.postgresSQLconnection.connect_tcp import connect_tcp_socket
from app.data.postgresSQLconnection.standard import standard_connect

SessionLocal = sessionmaker(bind=connect_with_connector(), autocommit=False, autoflush=False, )

Base = declarative_base()


def getDataBase():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#https://github.com/GoogleCloudPlatform/python-docs-samples/tree/7fb9175993fd3bb0511ca1bdb0612d8768f9a0a3/cloud-sql/postgres/sqlalchemy