import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.api.favorite import router as favorite_router
from app.api.note import router as notes_router
from app.api.tag import router as tags_router
from app.api.token import router as token_router
from app.api.user import router as users_router
from app.schemas import error_response

# 控制是否在生产环境暴露接口文档
EXPOSE_DOCS = os.getenv("EXPOSE_DOCS", "false").lower() == "true"
docs_url = "/docs" if EXPOSE_DOCS else None
redoc_url = None
openapi_url = "/openapi.json" if EXPOSE_DOCS else None

app = FastAPI(docs_url=docs_url, redoc_url=redoc_url, openapi_url=openapi_url)
app.include_router(users_router)
app.include_router(notes_router)
app.include_router(token_router)
app.include_router(tags_router)
app.include_router(favorite_router)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:4173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(status_code=500,
                        content=error_response(code=500, msg="Database error"))


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500,
                        content=error_response(code=500,
                                               msg="Internal server error"))
