from fastapi.security import OAuth2PasswordBearer
from fastapi import Header, Depends, HTTPException
from fastapi.responses import JSONResponse
from core.jwt_config import decode_access_token
from core.token_blacklist import token_in_blacklist
from db.models import user
from db.orm_funcs import Users, SessionLocal

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):

    if token_in_blacklist(token=token):
        raise HTTPException(status_code=401, detail="Token has been revoked. Please login again")

    payload=decode_access_token(token=token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Token payload invalid")
    
    session=SessionLocal()
    user=session.query(Users).filter(username==Users.username).first()
    session.close()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user  # full user object
