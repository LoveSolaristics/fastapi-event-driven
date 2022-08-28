from uvicorn import run


if __name__ == "__main__":  # pragma: no cover
    run(
        "app:app",
        host="127.0.0.1",
        port=8080,
        reload=True,
        reload_dirs=["delivery_hub", "tests"],
        log_level="debug",
    )
