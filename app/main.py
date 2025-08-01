import httpx
import uvicorn

from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from contextlib import asynccontextmanager

from app.config import settings
# from app.services.auth import parse_auth
from app.routers.vacancy_methods import router as vacancy_router
from app.routers.vacancies_methods import router as vacancies_router
from app.schemas.response_schemas import ResponseDetail, ExceptionDetail



@asynccontextmanager
async def lifespan(app: FastAPI):
    app.requests_client = httpx.AsyncClient(timeout=20)
    # app.state.auth_config = parse_auth()
    print("Service startup...")
    yield
    await app.requests_client.aclose()


app = FastAPI(
    title="Сервис управления вакансиями",
    lifespan=lifespan,
    version=settings.VERSION
)

app.include_router(vacancy_router)
app.include_router(vacancies_router)

origins = settings.ALLOWED_HOSTS.split()

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    error_type = exc.errors()[0].get('type')
    location = exc.errors()[0].get('loc')
    message = exc.errors()[0].get('msg')
    request_input = exc.errors()[0].get('input')
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            ExceptionDetail(
                detail=ResponseDetail(
                    code="BAD_REQUEST",
                    message=f'Type: {error_type}, location: {location}. {message}. Input: {request_input}'
                )
            )
        )
    )

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True
    )
