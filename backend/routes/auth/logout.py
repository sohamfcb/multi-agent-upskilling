from fastapi import (
    FastAPI,
    HTTPException,
    APIRouter,
    Depends,
    Request
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
from datetime import datetime

from core.auth_dependency import get_current_user
from core import token_blacklist

logger=get_logger("login")

logout_route=APIRouter(prefix="/auth")

@logout_route.post("/logout")
def logout(request: Request, user: str = Depends(get_current_user)):
    auth_header=request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer"):
        raise HTTPException(status_code=401, detail="missing or invalid token")
    
    token=auth_header.split(" ")[1]
    token_blacklist.blacklist_token(token=token)

    return JSONResponse(content={"message": "logged out successfully"})


@logout_route.delete("/de-register")
def delete_account(user: str = Depends(get_current_user), db: Session = Depends(get_db)):  
    try:
        db.delete(user)
        db.commit()

        logger.warning(f"User {user.username} deactivated their account")
        return JSONResponse(
            status_code=200,
            content={
                "status": True,
                "message": "account deactivated",
                "data": None
            }
        )
        
    except Exception as e:
        logger.error(f"{str(e)}")
        logger.warning("rollback initiated")
        db.rollback()
        logger.info("rollback successful")
        
        return JSONResponse(
            status_code=500,
            content={
                "status": False,
                "message": "Internal Server Error",
                "data": None
            }
        )