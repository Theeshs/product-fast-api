from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware



from core.routes import products


def create_app() -> FastAPI:
    app = FastAPI()
    origins = [
        "*"
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    app.include_router(
        products.router,
        prefix="/api",
    )

    return app


app = create_app()
