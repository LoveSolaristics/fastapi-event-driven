from uvicorn import run

from delivery_hub.config import get_settings


if __name__ == "__main__":  # pragma: no cover
    settings = get_settings()
    run(
        "delivery_hub.app:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True,
        reload_dirs=["delivery_hub", "tests"],
        log_level="debug",
    )
