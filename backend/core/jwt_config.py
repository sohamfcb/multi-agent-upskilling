from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib import hash
from passlib.context import CryptContext
from werkzeug.security import generate_password_hash, check_password_hash

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY=os.getenv("JWT_SECRET_KEY")
REFRESH_SECRET_KEY=os.getenv("JWT_SECRET_KEY_REFRESH")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES=int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))

def hash_password(password: str):
    return generate_password_hash(password)

def verify_password(plain, hashed):
    return check_password_hash(hashed, plain)

def create_access_token(data: dict, tv: int, expires_delta: timedelta = None):
    payload=data.copy()
    payload["tv"]=tv
    expiry=datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload.update({"exp":expiry})

    encoded_payload=jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_payload

def decode_access_token(token: str):
    try:
        decoded_token=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    
    except JWTError as err:
        print(str(err))
        return None
    
def create_refresh_token(data: dict, expires_delta: timedelta = None):
    payload=data.copy()

    expiry=datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES))
    payload.update({"exp": expiry})

    encoded_payload=jwt.encode(payload, REFRESH_SECRET_KEY, ALGORITHM)

    return encoded_payload

def decode_refresh_token(token: str):
    try:
        decoded_token=jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    
    except JWTError as err:
        print(str(err))
        return None