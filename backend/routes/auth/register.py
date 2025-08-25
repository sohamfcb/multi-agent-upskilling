from fastapi import (
    FastAPI,
    HTTPException,
    APIRouter,
    Depends
)
from fastapi.responses import JSONResponse
from schema import (
    user,
    user_profile
)
from db.models.orm_funcs import (
    SessionLocal,
    Users,
    UserProfile,
    get_db
)
import core.jwt_config as security
from sqlalchemy.orm import Session
from core.logger_config import get_logger
import time
import os
from utils import send_email_otp

from dotenv import load_dotenv

load_dotenv()

logger=get_logger("register")

COOLDOWN_SECONDS=60
EXPIRY_SECONDS=int(os.getenv("EXPIRY_SECONDS"))

auth_route=APIRouter(prefix="/auth")

# db_=SessionLocal()

otp_store={}
pending_signups = {}  

# @auth_route.post("/register")
# def register(payload: user.UserIn, db: Session = Depends(get_db)):
#     try:
#         email=db.query(Users).filter(Users.email==payload.email).first()
#         username=db.query(Users).filter(Users.username==payload.username).first()

#         if email or username:
#             logger.error(f"User with the same username/email exists")
#             # raise HTTPException(status_code=400, detail="User already exists.")
#             return JSONResponse(
#                 status_code=400,
#                 content={
#                     "status": False,
#                     "message": "user already exists",
#                     "data": None
#                 }
#             )

#         password_hash=security.hash_password(password=payload.password)
#         new_user = Users(
#             first_name=payload.first_name,
#             last_name=payload.last_name,
#             email=payload.email,
#             username=payload.username,
#             password=password_hash
#         )

#         db.add(new_user)
#         db.commit()

#         logger.info(f"User {payload.username} added successfully")

#         return JSONResponse(
#             content={"status": True,
#                     "message": "user registered successfully!",
#                     "data": None},
#             status_code=200
#         )
    
#     except Exception as e:
#         logger.error(str(e))
#         print(e)
#         db.rollback()
#         return JSONResponse(
#             status_code=500,
#             content={
#                 "status": False,
#                 "message": "internal server error",
#                 "data": None
#             }
#         )

@auth_route.post("/register")
def register(payload: user.UserIn,  db: Session = Depends(get_db)):
    # check if user already exists
    existing = db.query(Users).filter(
        (Users.email == payload.email) | (Users.username == payload.username)
    ).first()
    if existing:
        return JSONResponse(status_code=400,
            content={"status": False,"message": "user already exists","data": None}
        )

    # cooldown check
    now = time.time()
    if payload.email in pending_signups:
        last_sent = pending_signups[payload.email]["time"]
        if now - last_sent < COOLDOWN_SECONDS:
            return JSONResponse(status_code=429,
                content={"status": False,
                         "message": f"please wait {int(COOLDOWN_SECONDS - (now - last_sent))}s before requesting another code",
                         "data": None}
            )

    # generate OTP
    import random
    code = str(random.randint(100000, 999999))

    # save pending signup (with user info + otp)
    pending_signups[payload.email] = {
        "code": code,
        "time": now,
        "data": {
            "first_name": payload.first_name,
            "last_name": payload.last_name,
            "username": payload.username,
            "password": security.hash_password(payload.password)
        }
    }

    # send mail
    send_email_otp(email=payload.email, code=code)

    return JSONResponse(
        content={"status": True,
                 "message": "otp sent to your email. verify to complete registration",
                 "data": {"email": payload.email}},
        status_code=200
    )


@auth_route.post("/verify-signup")
def verify_signup(body: user.VerifySignUp, db: Session = Depends(get_db)):
    if body.email not in pending_signups:
        return JSONResponse(status_code=400,
            content={"status": False,"message": "no signup pending for this email","data": None}
        )

    record = pending_signups[body.email]
    now = time.time()

    # expiry
    if now - record["time"] > EXPIRY_SECONDS:
        del pending_signups[body.email]
        return JSONResponse(status_code=400,
            content={"status": False,"message": "code expired","data": None}
        )

    # match
    if body.code != record["code"]:
        return JSONResponse(status_code=400,
            content={"status": False,"message": "invalid code","data": None}
        )

    # ✅ success → create user in DB
    data = record["data"]
    new_user = Users(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=body.email,
        username=data["username"],
        password=data["password"],
        is_verified=True
    )
    db.add(new_user)
    db.commit()
    del pending_signups[body.email]

    return JSONResponse(status_code=200,
        content={"status": True,"message": "registration complete","data": None}
    )
