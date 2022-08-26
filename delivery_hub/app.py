from endpoints import routers_lists_with_prefixes
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware


def bind_routes(
    application: FastAPI,
    list_of_routes: list[tuple[str, list[APIRouter]]],
) -> None:
    """
    Bind all routes to application.
    """
    for prefix, routers in list_of_routes:
        for router in routers:
            application.include_router(router, prefix=prefix)


def bind_middlewares(application: FastAPI) -> None:
    application.add_middleware(
        CORSMiddleware, allow_origins=["http://localhost:3000"], allow_methods=["*"], allow_headers=["*"]
    )


def create_application() -> FastAPI:
    fastapi_app = FastAPI(
        title="DeliveryHub",
        description="Like DeliveryClub but better",
        docs_url="/swagger",
        openapi_url="/openapi",
        version="0.1.0",
    )
    bind_routes(fastapi_app, routers_lists_with_prefixes)
    bind_middlewares(fastapi_app)

    return fastapi_app


app = create_application()
