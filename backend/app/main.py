from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.routers.note import router as notes_router
from app.routers.token import router as token_router
from app.routers.user import router as users_router
from app.routers.tag import router as tags_router

from app.utils.response import error_response

app = FastAPI()
app.include_router(users_router)
app.include_router(notes_router)
app.include_router(token_router)
app.include_router(tags_router)


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(status_code=500,
                        content=error_response(code=500, msg="Database error"))


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500,
                        content=error_response(code=500,
                                               msg="Internal server error"))
