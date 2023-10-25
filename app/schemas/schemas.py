from typing import Optional
from pydantic import BaseModel


class User(BaseModel):

    name: str
    xgrowKey: str
    userType: bool
    password: str

    class Config():
        orm_mode = True


class Device(User):
    class Config():
        orm_mode = True

class ShowDevice(BaseModel):
    name: str
    userType: bool
    xgrowKey: str

    class Config():
        orm_mode = True

class ShowUser(BaseModel):
    name: str
    userType: bool
    xgrowKey: str

    class Config():
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str

class Settings(BaseModel):
    #PRODUCTION SETTINGS
    authjwt_secret_key: str = "WG%YR@#FG%%vw544wh5$#$$#"
    # Configure application to store and get JWT from cookies
    authjwt_token_location: set = {"cookies"}
    # Only allow JWT cookies to be sent over https
    authjwt_cookie_secure: bool = True
    # Enable csrf double submit protection. default is True
    authjwt_cookie_csrf_protect: bool = True
    # Change to 'lax' in production to make your website more secure from CSRF Attacks, default is None
    authjwt_cookie_samesite: str = 'lax'

    # DEVEOPER SETTINGS
    # authjwt_secret_key: str = "secret"
    # # Configure application to store and get JWT from cookies
    # authjwt_token_location: set = {"cookies"}
    # # Only allow JWT cookies to be sent over https
    # authjwt_cookie_secure: bool = False
    # # Enable csrf double submit protection. default is True
    # authjwt_cookie_csrf_protect: bool = True
    # # Change to 'lax' in production to make your website more secure from CSRF Attacks, default is None
    # # authjwt_cookie_samesite: str = 'lax'
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    name: Optional[str] = None
