from fastapi import (
    FastAPI,
    HTTPException,
    APIRouter,
    Depends
)
from fastapi.responses import JSONResponse
from db.models import (
    user,
    user_profile
)
from db.orm_funcs import (
    SessionLocal,
    Users,
    UserProfile,
    get_db
)
import core.jwt_config as security
from sqlalchemy.orm import Session
from core.logger_config import get_logger
from datetime import datetime

logger=get_logger("login")

login_route=APIRouter(prefix="/auth")

# db_=SessionLocal()

@login_route.post("/login", response_model=user.TokenResponseSchema)
def register(payload: user.Login, db: Session = Depends(get_db)):
    try:
        email=db.query(Users).filter(Users.email==payload.email).first()
        username=db.query(Users).filter(Users.username==payload.username).first()

        email_or_username=email or username

        if not email_or_username:
            logger.error(f"User doesn't exist")
            return JSONResponse(
                status_code=400,
                content={
                    "status": False,
                    "message": "User does not exist.",
                    "data": None
                }
            )
        
        if security.verify_password(hashed=email_or_username.password, plain=payload.password):
            logger.info(f"User {payload.username} logged in successfully at {datetime.now()}")

            email_or_username.last_login=datetime.now()
            db.commit()

            token_payload={"sub": email_or_username.username}
            access_token=security.create_access_token(data=token_payload)
            refresh_token=security.create_refresh_token(data=token_payload)

            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
            }

        logger.error(f"User {payload.username} entered a wrong password")
        return JSONResponse(
            status_code=400,
            content={
                "status": False,
                "message": "Wrong password. Try again",
                "data": None
                }
            )
    
    except Exception as e:
        logger.error(str(e))
        print(e)
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={
                "status": False,
                "message": "internal server error",
                "data": None
            }
        )