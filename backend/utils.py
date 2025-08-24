from typing import Any
from fastapi.responses import JSONResponse

def return_response(message: str, status: bool = False, data: Any = None, status_code: int = 200):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": status,
            "message": message,
            "data": data
        }
    )