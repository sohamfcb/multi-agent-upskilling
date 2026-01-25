from fastapi import FastAPI, Request, Depends
from routes.auth.register import auth_route
from routes.auth.login import login_route
from routes.auth.logout import logout_route
from routes.auth.update import update_route
from routes.core.resume_reader import resume_reader_route

from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import time
from core.logger_config import get_logger, init_logging
from core.auth_dependency import get_current_user
from routes.core.chatbot import bot_route

from prometheus_fastapi_instrumentator import Instrumentator

logger=get_logger("uvicorn.access")

init_logging()

app=FastAPI()

Instrumentator().instrument(app=app).expose(app=app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for specific frontend
    allow_credentials=True,
    allow_methods=["*"],  # ["GET", "POST", "PUT", "DELETE"]
    allow_headers=["*"],
)

app.include_router(auth_route)
app.include_router(login_route)
app.include_router(logout_route)
app.include_router(update_route)
app.include_router(bot_route)
app.include_router(resume_reader_route)


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

