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
from utils import send_email_otp, return_response

from dotenv import load_dotenv

load_dotenv()

logger=get_logger("register")

COOLDOWN_SECONDS=int(os.getenv("COOLDOWN_SECONDS"))
EXPIRY_SECONDS=int(os.getenv("EXPIRY_SECONDS"))
OTP_LIMIT=int(os.getenv("OTP_LIMIT"))

auth_route=APIRouter(prefix="/auth")

# db_=SessionLocal()

otp_store={}
pending_signups = {}  

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

    pending_signups[payload.email]["count"]=0

    # send mail
    send_email_otp(email=payload.email, code=code)
    # time_after_mail_sent=now()

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

    if pending_signups[body.email]["count"]==OTP_LIMIT:
        return return_response(message="OTP limit reached. Register again.", status_code=400)

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
