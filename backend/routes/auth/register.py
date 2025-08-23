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

logger=get_logger("register")

auth_route=APIRouter(prefix="/auth")

# db_=SessionLocal()

@auth_route.post("/register")
def register(payload: user.UserIn, db: Session = Depends(get_db)):
    try:
        email=db.query(Users).filter(Users.email==payload.email).first()
        username=db.query(Users).filter(Users.username==payload.username).first()

        if email or username:
            logger.error(f"User with the same username/email exists")
            # raise HTTPException(status_code=400, detail="User already exists.")
            return JSONResponse(
                status_code=400,
                content={
                    "status": False,
                    "message": "user already exists",
                    "data": None
                }
            )
        
        password_hash=security.hash_password(password=payload.password)
        new_user = Users(
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            username=payload.username,
            password=password_hash
        )

        db.add(new_user)
        db.commit()

        logger.info(f"User {payload.username} added successfully")

        return JSONResponse(
            content={"status": True,
                    "message": "user registered successfully!",
                    "data": None},
            status_code=200
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