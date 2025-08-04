from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer
from typing import Optional
from ..database.connection import mongo

from config import Config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# hybrid approach for JWT in cookie
class CookieBearer(HTTPBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        cookie_token = request.cookies.get("access_token")
        if cookie_token:
            if cookie_token.startswith("Bearer "):
                return cookie_token[7:]
            return cookie_token
        
        """Fallback to Authorization header for API clients
        authorization = request.headers.get("Authorization")
        if authorization:
            scheme, token = authorization.split(" ", 1)
            if scheme.lower() == "bearer":
                return token"""
        
        raise HTTPException(status_code=401, detail="Not authenticated")

oauth2_scheme = CookieBearer()


def verify_password(plain_password, hashed):
    return pwd_context.verify(plain_password, hashed)

def hash_password(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.SECRET_ALGORITHM)

def decode_access_token(token: str):
    return jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.SECRET_ALGORITHM])


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = await mongo.db["users"].find_one({"username": username})
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")