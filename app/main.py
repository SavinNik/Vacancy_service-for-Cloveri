import httpx
import uvicorn
import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
# from app.services.auth import parse_auth
from app.routers.vacancy_methods import router as vacancy_router
from app.routers.vacancies_methods import router as vacancies_router


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.requests_client = httpx.AsyncClient(timeout=20)
    # app.state.auth_config = parse_auth()
    logger.info("Service startup...")
    yield
    await app.requests_client.aclose()
    logger.info("Service shutdown...")


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


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Глобальный обработчик исключений: {exc}", exc_info=True)
    raise exc


# if __name__ == '__main__':
#     uvicorn.run(
#         'main:app',
#         host='0.0.0.0',
#         port=8000,
#         reload=True
#     )
