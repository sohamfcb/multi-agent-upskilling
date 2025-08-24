from fastapi import (
    FastAPI,
    HTTPException,
    APIRouter,
    Depends,
    Request
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

from core.auth_dependency import get_current_user
from core import token_blacklist

from utils import return_response

logger=get_logger("update-user-details")

update_route=APIRouter(prefix="/auth")

@update_route.put("/update-username")
def update_username(payload: user.UpdateUsername, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        existing_username=db.query(Users).with_entities(Users.username).filter(Users.username==user.username).first()

        if existing_username==payload.new_username:
            logger.warning(f"User with id {user.id} tried to update their username with their existing username itself")
            return return_response(message="New username cannot be the same as the old one", status_code=400)
        
        if db.query(Users).filter(Users.username==payload.new_username).first():
            logger.error(f"Username {payload.new_username} not available")
            return return_response(message=f"Username {payload.new_username} not available", status_code=400)

        db.query(Users).filter(Users.username==user.username).update({"username": payload.new_username, "updated_at": datetime.now()})
        db.commit()

        logger.info(f"Username for user {user.username} changed to {payload.new_username}")
        return return_response(message="username updated successfully", status= True)
    
    except Exception as e:
        logger.error(f"{str(e)}")
        return return_response(message="Internal Server Error", status_code=500)
    

@update_route.put("/change-password")
def change_password(payload: user.UpdatePassword, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        if security.verify_password(hashed=db.query(Users).with_entities(Users.password).filter(Users.username==user.username).first()[0], plain=payload.new_password):
            logger.warning(f"User {user.username} tried to update existing password with the existing passsword itself")
            return return_response(message="New password cannot be the same as the old one", status_code=400)
        
        new_password_hash=security.hash_password(password=payload.new_password)

        db.query(Users).filter(Users.email==user.email).update({"password": new_password_hash, "updated_at": datetime.now(), "token_version": Users.token_version+1}, synchronize_session=False)
        db.commit()

        logger.info(f"User {user.username} changed their password.")
        return return_response(message="Password changed successfully", status_code=200, status=True)
    
    except Exception as e:
        logger.error(f"{str(e)}")
        return return_response(message="Internal Server Error", status_code=500)