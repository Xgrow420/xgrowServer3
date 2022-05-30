from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel

from datetime import datetime, timedelta
from jose import JWTError, jwt

from app.main import app
from app.schemas import schemas
from app.schemas.schemas import Settings, User

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    '''verify token and return TokenData model'''
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get("sub")
        if name is None:
            raise credentials_exception
        return schemas.TokenData(name=name)
    except JWTError:
        raise credentials_exception
    
    
    

"""
By default, the CRSF cookies will be called csrf_access_token and
csrf_refresh_token, and in protected endpoints we will look
for the CSRF token in the 'X-CSRF-Token' headers. only certain
methods should define CSRF token in headers default is ('POST','PUT','PATCH','DELETE')
"""

@AuthJWT.load_config
def get_config():
    return Settings()

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

@app.post('/login')
def login(user: User, Authorize: AuthJWT = Depends()):
    """
    With authjwt_cookie_csrf_protect set to True, set_access_cookies() and
    set_refresh_cookies() will now also set the non-httponly CSRF cookies
    """
    if user.name != "test" or user.password != "test":
        raise HTTPException(status_code=401,detail="Bad username or password")

    # Create the tokens and passing to set_access_cookies or set_refresh_cookies
    access_token = Authorize.create_access_token(subject=user.name)
    refresh_token = Authorize.create_refresh_token(subject=user.name)

    # Set the JWT and CSRF double submit cookies in the response
    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    return {"msg":"Successfully login"}

@app.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    # Set the JWT and CSRF double submit cookies in the response
    Authorize.set_access_cookies(new_access_token)
    return {"msg":"The token has been refresh"}

@app.delete('/logout')
def logout(Authorize: AuthJWT = Depends()):
    """
    Because the JWT are stored in an httponly cookie now, we cannot
    log the user out by simply deleting the cookie in the frontend.
    We need the backend to send us a response to delete the cookies.
    """
    Authorize.jwt_required()

    Authorize.unset_jwt_cookies()
    return {"msg":"Successfully logout"}

@app.get('/protected')
def protected(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}

