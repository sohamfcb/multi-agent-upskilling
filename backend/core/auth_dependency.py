# from fastapi.security import OAuth2PasswordBearer
# from fastapi import Header, Depends, HTTPException
# from fastapi.responses import JSONResponse
# from core.jwt_config import decode_access_token
# from core.token_blacklist import token_in_blacklist
# from db.models import user
# from db.orm_funcs import Users, SessionLocal

# oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/auth/login")

# def get_current_user(token: str = Depends(oauth2_scheme)):
#     if token_in_blacklist(token=token):
#         raise HTTPException(status_code=401, detail="Token has been revoked. Please login again")

#     payload=decode_access_token(token=token)

#     if not payload:
#         raise HTTPException(status_code=401, detail="Invalid or expired token")
    
#     username = payload.get("sub")
#     tv=payload.get("tv")
#     if not username:
#         raise HTTPException(status_code=401, detail="Token payload invalid")
    
#     session=SessionLocal()
#     user=session.query(Users).filter(Users.username==username).first()
#     # session.close()

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     if tv!=user.token_version:
#         raise HTTPException(status_code=401, detail="Token expired")

#     return user  # full user object

# auth_dependency.py
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import JWTError
from jose.exceptions import ExpiredSignatureError
from sqlalchemy.orm import Session

from core.jwt_config import decode_access_token
from core.token_blacklist import token_in_blacklist
from db.orm_funcs import Users, get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    # 1) Blacklist check (logout-now / rotate cred scenarios)
    if token_in_blacklist(token=token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 2) Decode + validate exp/signature
    try:
        payload = decode_access_token(token)  # should raise on bad/expired if you re-raise in decode
        if not payload:
            # decode_access_token returned None -> invalid token format/signature
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token.",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token expired.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3) Extract claims
    username = payload.get("sub")
    tv = payload.get("tv")
    if not username:
        raise HTTPException(status_code=401, detail="Token payload invalid.")

    # 4) Load user (correct filter!)
    db_user = db.query(Users).filter(Users.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")

    # 5) Enforce token_version (logout-all-sessions support)
    if tv is None or tv != db_user.token_version:
        # Not time expiry; it’s a version bump (user logged out everywhere)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token version mismatch. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return db_user
