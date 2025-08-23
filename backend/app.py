from fastapi import FastAPI, Request, Depends
from routes.auth.register import auth_route
from routes.auth.login import login_route
from routes.auth.logout import logout_route
from fastapi.responses import JSONResponse

import time
from core.logger_config import get_logger
from core.auth_dependency import get_current_user

logger=get_logger("uvicorn.access")

app=FastAPI()
app.include_router(auth_route)
app.include_router(login_route)
app.include_router(logout_route)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    logger.info(
        f"{request.method} {request.url.path} "
        f"Status={response.status_code} "
        f"Time={process_time:.2f}ms"
    )
    return response

@app.get("/")
def home(user: str = Depends(get_current_user)):
    return JSONResponse({"message": "hello"})

