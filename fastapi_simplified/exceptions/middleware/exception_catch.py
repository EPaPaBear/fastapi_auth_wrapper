from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi_simplified.exceptions.resource_exceptions import *
from sqlalchemy.exc import IntegrityError
#from main import app

#@app.middleware("http")
async def exceptions_middleware(request : Request, call_next):
    try:
        response = await call_next(request)
        return response
    except IntegrityError as e:
        return JSONResponse(status_code=400, content={"message": "Database Integrity Error: " + str(e)})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})
