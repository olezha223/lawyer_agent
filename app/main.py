import uvicorn

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
from dishka.integrations.fastapi import setup_dishka

from src.api import router
from src.di import container
from src.shared.config import config


def create_fastapi_app() -> FastAPI:
    app = FastAPI(title="ИИ-агент для анализа договоров на риски для клиента.",)

    app.include_router(router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.ALLOW_ORIGINS.split(),
        allow_credentials=bool(config.ALLOW_CREDENTIALS),
        allow_methods=config.ALLOW_METHODS.split(),
        allow_headers=config.ALLOW_HEADERS.split(),
    )

    app.openapi_schema = get_openapi(
        title="agent",
        version="1.0",
        routes=app.routes,
    )

    return app


app = create_fastapi_app()
setup_dishka(container, app)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
