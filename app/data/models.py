from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Enum, ARRAY
from sqlalchemy.orm import relationship
from typing import List

from app.data.database import Base


# DATABASE MODEL


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    xgrowKey = Column(String)
    userType = Column(Boolean)
    password = Column(String)

    # PotList = Column(List)

    #preferences = relationship("Preferences", back_populates="creator")



# tabela xgrowkeys jest wpisywana recznie i definiuje klucz xgrow ktory moze polaczyc sie z serwisem, jesli
#klucz nie znajduje sie w bazie to urzadzenie sie nie polaczy z serwerem !
class XgrowKeys(Base):
    __tablename__ = 'xgrowKeys'

    id = Column(Integer, primary_key=True, index=True)
    xgrowKey = Column(String)
    #device Section
    ban = Column(Boolean)
    reason = Column(String)
    subscription = Column(Integer)

#tabela SubscriptionKeys jest wpisywana recznie i zawiera kody do przedluzania subskrypcji
class SubscriptionKeys(Base):

    __tablename__ = 'subscriptionKeys'

    id = Column(Integer, primary_key=True, index=True)
    subscriptionKey = Column(String)
    days = Column(Integer)
    released = Column(Boolean)





