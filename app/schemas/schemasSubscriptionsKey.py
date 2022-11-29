from pydantic import BaseModel


class SubscriptionKey(BaseModel):

    subscriptionsKey: str
    days: int
    released: bool

    class Config():
        orm_mode = True

